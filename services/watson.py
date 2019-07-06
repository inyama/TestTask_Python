import ibm_watson


class WatsonProcessor:
    def __init__(self, personality_url, personality_key, translator_url, translator_key):
        self.personality = ibm_watson.PersonalityInsightsV3(
            version='2017-10-13',
            url=personality_url,
            iam_apikey=personality_key)
        self.language_translator = ibm_watson.LanguageTranslatorV3(
            version='2018-05-01',
            url=translator_url,
            iam_apikey=translator_key)

    def detect_language(self, text, max_text_size):
        detect = text
        if len(text) > max_text_size:
            detect = text[:max_text_size]
        return self.language_translator.identify(detect).get_result()

    def get_insights(self, text, language, default_language):
        return self.personality.profile(
            text,
            accept='text/csv',
            csv_headers=True,
            content_language=language,
            raw_scores=True,
            language=default_language).get_result()
