import logging
import os
from unittest import TestCase

from utils.utils import clean_text, add_to_csv

from unittest.mock import MagicMock, Mock


class TestUtils(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_name_output = "output.csv"

    def test_add_to_csv(self):
        content = Mock()
        content.decode = MagicMock(return_value="header\ncontent")
        add_to_csv("test", content, self.file_name_output)
        with open(self.file_name_output, "r", newline='') as csv_file:
            content_check = csv_file.read()
        self.assertEqual(content_check, "test,content\r\n")

    def test_clean_text(self):
        processed_test = clean_text("http://test.site @mention")
        self.assertEqual(processed_test, " ")

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.file_name_output)
        except IOError:
            logging.warning("File was already removed")
