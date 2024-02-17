class NotFoundModelException(Exception):
    def __init__(self, speaker_name: str):
        self.speaker_name = speaker_name
        super().__init__(f"Model not found for speaker: {speaker_name}")

class NotCorrectTextException(Exception):
    def __init__(self, text: str):
        self.text = text
        super().__init__(f"Text not correct: {text}")

class TextTooLongException(Exception):
    def __init__(self, text: str):
        self.text = text
        super().__init__(f"Text too long. Length is {len(text)}. Max length is 930 symbols.")

class InvalidSampleRateException(Exception):
    def __init__(self, sample_rate: int) -> None:
        self.sample_rate = sample_rate
        super().__init__(f"Invalid sample rate {sample_rate}. Supported sample rates are 8 000, 24 000, and 48 000.")
