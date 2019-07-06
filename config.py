import os

ACCESS_TOKEN_KEY = os.environ.get("ACCESS_TOKEN_KEY", "220739081-OviHc78suwjR0GnXWIAoPzl6VzZdlJhCVMAlMk7A")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET", "MINdKpbShgLUQ0oslI9CQ8kTTDatw9K5FpnOdg5AI2Qlu")

CONSUMER_KEY = os.environ.get("CONSUMER_KEY", "6gTE57NKlIQdcqyfSAJMnWkNi")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET", "Y3XSTCujMQpSxJe3GPFpG93nMjBBsgKILfZdUPcRaOpS37NAYF")

DELAY = os.environ.get("DELAY", 1)
THREAD_DELAY = 1
WATSON_LANGUAGE_KEY = os.environ.get("WATSON_LANGUAGE_KEY", "zg3bzS5uzuTpDpDthAYIokUokA9B_cTfB38z_Y3vjWKi")
WATSON_LANGUAGE_URL = os.environ.get("WATSON_LANGUAGE_URL",
                                     "https://gateway-lon.watsonplatform.net/language-translator/api")
# WATSON_PERSONALITY_KEY = os.environ.get("WATSON_PERSONALITY_KEY", "_I2n_y_UTWaQmdm3y9VtLLcHt5_1ssntfCPfiOFj5neb")
WATSON_PERSONALITY_KEY = os.environ.get("WATSON_PERSONALITY_KEY", "ImkgYqGT94BlAHKcKL_vScw0eM2Kvk6NhxV8LMXdebWk")
WATSON_PERSONALITY_URL = os.environ.get("WATSON_PERSONALITY_URL",
                                        "https://gateway-lon.watsonplatform.net/personality-insights/api")
MAX_TEXT_SIZE = os.environ.get("MAX_TEXT_SIZE", 20*1024)
MAX_TEXT_SIZE_PREDICT = os.environ.get("MAX_TEXT_SIZE_PREDICT", 80000)
TWEETS_PER_PAGE = os.environ.get("TWEETS_PER_PAGE ", 200)
DEFAULT_OUTPUT_LANG = os.environ.get("DEFAULT_OUTPUT_LANG", "en")
OUTPUT_FILE=os.environ.get("OUTPUT_FILE", "output.csv")
ALLOWED_LANGUAGES = ["en", "es", "ja", "ar", "ko"]
