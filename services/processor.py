import csv
import logging
import threading
from multiprocessing import Queue
from time import sleep

import sys

from ibm_cloud_sdk_core import ApiException
from twitter import TwitterError

import config
from services.twitter import TwitterProcessor
from services.watson import WatsonProcessor
import os
from utils.utils import clean_text, add_to_csv, parallel_file_read, write_csv_queue


class ProcessingError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class Insight:
    def __init__(self, account, insight):
        self.account = account
        self.insight = insight


class Processor:
    def __init__(self, twitter_file=None):
        if twitter_file is None:
            self.twitter = TwitterProcessor(config.CONSUMER_KEY, config.CONSUMER_SECRET,
                                            config.ACCESS_TOKEN_KEY, config.ACCESS_TOKEN_SECRET)
        else:
            self.stop_event = threading.Event()
            self.queue_input = Queue()
            self.queue_output = Queue()
            self.queue_finish = Queue()
            self.lock = threading.Lock()

            with open(twitter_file, newline='') as csv_file:
                keys = csv.reader(csv_file, delimiter=',')
                self.twitters = []
                for key in keys:
                    self.twitters.append(TwitterProcessor(key[0], key[1], key[2], key[3]))

        self.watson = WatsonProcessor(config.WATSON_PERSONALITY_URL, config.WATSON_PERSONALITY_KEY,
                                      config.WATSON_LANGUAGE_URL,
                                      config.WATSON_LANGUAGE_KEY)

    def run_with_params(self, params):
        start_from = 0
        output_filename = config.OUTPUT_FILE
        if params.output is not None:
            output_filename = params.output
        if params.resume:
            try:
                with open('.index', 'r') as f_lock:
                    start_from = int(f_lock.readline())
            except IOError:
                logging.info("No prev activity found. Starting from the beginning.")
        if params.file is not None:
            try:
                with open(params.file, 'r') as f:
                    self.process_accounts(f, params, start_from, output_filename)
            except IOError as exc:
                logging.error("No prev activity found. Starting from the beginning." + str(exc))
        elif params.input is not None:
            self.process_accounts(params.input, params, start_from, output_filename)

    def run_with_params_parallel(self, params):
        output_filename = config.OUTPUT_FILE
        if params.output is not None:
            output_filename = params.output
        try:
            with open(output_filename, "w", newline=''):
                logging.info("Creating new file")
        except IOError as exc:
            logging.error(str(exc))
            sys.exit("Can not create output file. Exiting")
        if params.file is not None:
            self.__run_threads(params.file, output_filename, params)
        elif params.input is not None:
            self.__run_threads(params.file, output_filename, params, command_line_array=params.input)

    def __run_threads(self, input_file, output_file, params, command_line_array=None):
        jobs = []
        if command_line_array is not None:
            for item in command_line_array:
                self.queue_input.put(item)
            self.stop_event.set()
            jobs = [threading.Thread(target=write_csv_queue, args=(self.queue_output, self.queue_finish,
                                                                   len(self.twitters), output_file))]
        else:
            jobs.append(threading.Thread(target=parallel_file_read,
                                         args=(input_file, self.queue_input, self.stop_event)))
            jobs.append(threading.Thread(target=write_csv_queue, args=(self.queue_output, self.queue_finish,
                                                                       len(self.twitters), output_file)))
        for twitter in self.twitters:
            jobs.append(threading.Thread(target=self.process_accounts_queue, args=(twitter, params)))

        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

    def process_accounts_queue(self, twitter, params):
        while not self.queue_input.empty() or not self.stop_event.isSet():
            self.lock.acquire()
            item = False
            if not self.queue_input.empty():
                item = self.queue_input.get()
            self.lock.release()
            if item:
                self.process_account(current=item, params=params, output_filename=None, first_account=False,
                                     twitter=twitter)
            sleep(config.THREAD_DELAY)
        self.queue_finish.put(True)

    def process_accounts(self, twitter_accounts, params, start_from, output_filename):
        index = 0
        if start_from == 0:
            try:
                if params.ignore:
                    with open(output_filename, "w", newline=''):
                        logging.info("Creating new file")
                else:
                    with open(output_filename, "x", newline=''):
                        logging.info("Creating new file")
            except IOError as exc:
                logging.error(str(exc))
                sys.exit("Output file already present. Please remove or rename it and try again. Exiting")

        for current in twitter_accounts:
            current = current.strip(' \n')
            if index >= start_from:
                self.process_account(current, params, output_filename, index == 0)
            index += 1
            try:
                with open('.index', 'w') as f_lock:
                    f_lock.write(str(index))
            except IOError as exc:
                logging.error(str(exc))
                sys.exit("Index file couldn't be updated. Exiting")
        os.remove('.index')

    def process_account(self, current, params, output_filename=None, first_account=False, twitter=None):
        logging.info("Processing: " + current)
        sleep(config.DELAY)
        try:
            if twitter is not None:
                user_content = clean_text(twitter.get_tweets_text(current.split("/")[3]))
            else:
                user_content = clean_text(self.twitter.get_tweets_text(current.split("/")[3]))
            language = config.DEFAULT_OUTPUT_LANG
            if params.recognize:
                try:
                    lang = self.watson.detect_language(user_content, config.MAX_TEXT_SIZE)['languages']
                    language = lang[0]['language']
                    if language not in config.ALLOWED_LANGUAGES:
                        language = config.DEFAULT_OUTPUT_LANG
                except ApiException as exc:
                    logging.warning("Error on language detection." + str(exc))
                    raise ProcessingError
            try:
                insights = self.watson.get_insights(user_content, language, config.DEFAULT_OUTPUT_LANG)
                if twitter is not None:
                    self.queue_output.put(Insight(current, insights))
                else:
                    add_to_csv(current, insights.content, output_filename, first_account)
            except ApiException as exc:
                logging.warning("Can't get insights." + str(exc))
                raise ProcessingError
            except IOError as exc:
                logging.warning("Can't write to file." + str(exc))
                raise ProcessingError
        except (ProcessingError, TwitterError, ValueError) as exc:
            if params.ignore:
                logging.warning("Ignoring exception. Trying next twitter account." + str(exc))
            else:
                if twitter is None:
                    logging.info("Exiting" + str(exc))
                    sys.exit()
