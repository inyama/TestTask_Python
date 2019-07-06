from unittest import TestCase
from unittest.mock import MagicMock, Mock

from ibm_watson import PersonalityInsightsV3, LanguageTranslatorV3

from services.watson import WatsonProcessor


class TestWatson(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.personality = Mock(PersonalityInsightsV3)
        cls.translator = Mock(LanguageTranslatorV3)

        cls.watson = WatsonProcessor("", "", "", "")

    def test_detect_language(self):
        return_mock = Mock()
        return_mock.get_result = MagicMock(return_value=1)
        self.translator.identify = MagicMock(return_value=return_mock)
        self.watson.language_translator = self.translator
        self.assertEqual(self.watson.detect_language("test", 1), 1)
        self.assertEqual(len(self.translator.identify.mock_calls), 1)

    def test_get_insights(self):
        return_mock = Mock()
        return_mock.get_result = MagicMock(return_value=1)
        self.personality.profile = MagicMock(return_value=return_mock)
        self.watson.personality = self.personality
        self.assertEqual(self.watson.get_insights("test", "en", "en"), 1)
