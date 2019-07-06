import logging
import os
from unittest import TestCase

import config
from services import processor
from services.processor import Processor
from unittest.mock import MagicMock, Mock

from services.twitter import TwitterProcessor
from services.watson import WatsonProcessor


class TestProcessor(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.processor = Processor()

    def test_run_with_params_nothing_set(self):
        self.processor.process_accounts = MagicMock()
        params = Mock()
        params.file = None
        params.input = None
        self.processor.run_with_params(params)
        self.assertEqual(self.processor.process_accounts.call_count, 0)

    def test_run_with_params_wrong_file_set(self):
        self.processor.process_accounts = MagicMock()
        params = Mock()
        params.file = None
        params.input = "wrong.file"
        self.processor.run_with_params(params)
        self.assertEqual(self.processor.process_accounts.call_count, 1)

    def test_run_with_params_correct_input_set(self):
        self.processor.process_accounts = MagicMock()
        params = Mock()
        params.file = None
        params.input = "test_account"
        self.processor.run_with_params(params)
        self.assertEqual(self.processor.process_accounts.call_count, 1)

    def test_process_accounts(self):
        params = Mock()
        params.file = None
        params.input = "test_account"
        pr = Processor()
        pr.process_account = MagicMock()
        pr.process_accounts(["test"], params, 0, config.OUTPUT_FILE)
        self.assertEqual(pr.process_account.call_count, 1)

    def test_process_account_recongnize_language(self):
        params, watson, twitter, processor_account = self.get_mocks()
        params.recognize = True
        processor.add_to_csv = MagicMock()
        processor.clean_text = MagicMock(return_value="test test")
        processor_account.process_account("http://twitter.com/test_account", params, config.OUTPUT_FILE)
        self.assertEqual(watson.detect_language.call_count, 1)
        self.assertEqual(twitter.get_tweets_text.call_count, 1)
        self.assertEqual(processor.add_to_csv.call_count, 1)
        self.assertEqual(processor.clean_text.call_count, 1)

    def test_process_account_do_not_recognize_language(self):
        params, watson, twitter, processor_account = self.get_mocks()
        params.recognize = False
        processor.add_to_csv = MagicMock()
        processor.clean_text = MagicMock(return_value="test test")
        processor_account.process_account("http://twitter.com/test_account", params, config.OUTPUT_FILE)
        self.assertEqual(watson.detect_language.call_count, 0)
        self.assertEqual(twitter.get_tweets_text.call_count, 1)
        self.assertEqual(processor.add_to_csv.call_count, 1)
        self.assertEqual(processor.clean_text.call_count, 1)

    def get_mocks(self):
        return_language = {
            "languages": [
                {"language": "en"}
            ]
        }
        params = Mock()
        params.input = "test_account"
        watson = Mock(WatsonProcessor)
        watson.detect_language = MagicMock(return_value=return_language)
        skills = Mock()
        skills.content = "insights"
        watson.get_insights = MagicMock(return_value=skills)
        twitter = Mock(TwitterProcessor)
        twitter.get_tweets_text = MagicMock(return_value="test text")
        processor_account = Processor()
        processor_account.watson = watson
        processor_account.twitter = twitter

        return params, watson, twitter, processor_account

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(config.OUTPUT_FILE)
        except IOError:
            logging.warning("File was already removed")
