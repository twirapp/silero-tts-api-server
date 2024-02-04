class NotFoundModelException(Exception):
    def __init__(self, speaker_name: str):
        super().__init__(f"Model not found for speaker: {speaker_name}")

class NotCorrectTextException(Exception):
    def __init__(self, text: str):
        super().__init__(f"Text not correct: {text}")

class TextTooLongException(Exception):
    def __init__(self, text: str):
        super().__init__(f"Text too long. Length is {len(text)}. Max length is 930 symbols.")