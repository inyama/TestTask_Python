import csv
import re
from time import sleep

import config


def clean_text(user_content):
    processed = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', user_content, flags=re.MULTILINE)
    return re.sub('@[^\s]+', '', processed, flags=re.MULTILINE)


def add_to_csv(account_name, content, output_file, header=False):
    profile = content.decode("utf-8")
    csv_reader = csv.reader(profile.splitlines())
    csv_list = list(csv_reader)
    with open(output_file, "a+", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        if csv_list:
            if header:
                line = csv_list[0]
                line.insert(0, "account_name")
                writer.writerow(line)
            line = csv_list[1]
            line.insert(0, account_name)
            writer.writerow(line)


def parallel_file_read(file_name, process_queue, stop_event):
    with open(file_name, 'r') as twitter_accounts:
        for current in twitter_accounts:
            process_queue.put(current.strip(' \n'))
            sleep(config.THREAD_DELAY)
    stop_event.set()


def write_csv_queue(output_queue, finish_queue, worker_count, output_file):
    stop = False
    header = True
    while not stop and finish_queue.qsize() < worker_count:
        if not output_queue.empty():
            while not output_queue.empty():
                insight = output_queue.get()
                add_to_csv(insight.account, insight.insight.content, output_file, header)
                sleep(config.THREAD_DELAY)
                header = False
        if finish_queue.qsize() == worker_count:
            stop = True
