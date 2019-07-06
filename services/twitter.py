import twitter
from time import sleep

import config
from config import TWEETS_PER_PAGE, MAX_TEXT_SIZE_PREDICT


class TwitterProcessor:
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.api = twitter.Api(
            consumer_key, consumer_secret, access_token_key, access_token_secret
        )

    def get_tweets_text(self, screen_name=None, tweets_per_page=TWEETS_PER_PAGE,
                        max_predict_size=MAX_TEXT_SIZE_PREDICT):
        timeline = self.api.GetUserTimeline(screen_name=screen_name, count=tweets_per_page)
        earliest_tweet = min(timeline, key=lambda tweet: tweet.id).id
        size = sum([*map(lambda tweet: len(tweet.text), timeline)])
        while size < max_predict_size:
            sleep(config.DELAY)
            tweets = self.api.GetUserTimeline(
                screen_name=screen_name, max_id=earliest_tweet, count=tweets_per_page
            )
            size += sum([*map(lambda tweet: len(tweet.text), tweets)])
            new_earliest = min(tweets, key=lambda tweet: tweet.id).id
            if not tweets or new_earliest == earliest_tweet:
                break
            else:
                earliest_tweet = new_earliest
                timeline += tweets
        return ' '.join([*map(lambda tweet: tweet.text, timeline)])
