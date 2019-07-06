from unittest import TestCase
from unittest.mock import MagicMock, Mock
from twitter import Api
from services.twitter import TwitterProcessor


class TestTwitter(TestCase):
    def test_get_tweets_text(self):
        api = Mock(Api)
        return_mock = Mock()
        return_mock.id = 1
        return_mock.text = "test"
        api.GetUserTimeline = MagicMock(return_value=[return_mock])
        twitter = TwitterProcessor("", "", "", "")
        twitter.api = api
        self.assertEqual(twitter.get_tweets_text("test"), "test")
        self.assertEqual(len(api.GetUserTimeline.mock_calls), 2)
