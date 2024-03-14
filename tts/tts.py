from typing import TYPE_CHECKING
from pathlib import Path
from io import BytesIO

import torch
from torch.package import PackageImporter
import numpy as np

from tts.exceptions import *

if TYPE_CHECKING:
    from .typing.package import TTSModelMultiAcc_v3


# fixes import package error on Mac
# https://github.com/snakers4/silero-models/discussions/104
torch.backends.quantized.engine = "qnnpack"

MAX_INT16 = 32767

print(f"Using {torch.get_num_threads()} threads. To change, set environment variable MKL_NUM_THREADS")

device = torch.device("cpu")


class TTS:
    VALID_SAMPLE_RATES = (8000, 24000, 48000)

    def __init__(self):
        self.models: dict[str, "TTSModelMultiAcc_v3"] = {}
        self.speakers: dict[str, list[str]] = {}
        self.model_by_speaker: dict[str, "TTSModelMultiAcc_v3"] = {}

        for model_path in Path("models").glob("*.pt"):
            self._load_model(model_path)

    def generate(self, text: str, speaker: str, sample_rate: int) -> bytes:
        model = self.model_by_speaker.get(speaker)
        if not model:
            raise NotFoundModelException(speaker)
        if sample_rate not in self.VALID_SAMPLE_RATES:
            raise InvalidSampleRateException(sample_rate)

        text = self._delete_dashes(text)
        return self._generate_audio(model, text, speaker, sample_rate)

    def _load_model(self, model_path: Path):
        package = PackageImporter(model_path)
        model: "TTSModelMultiAcc_v3" = package.load_pickle("tts_models", "model")
        if model.device != device:
            model.to(device)

        language = model_path.stem[3:]  # remove prefix "v3_" or "v4_"
        self.models[language] = model

        self._load_speakers(model, language)

    def _load_speakers(self, model: "TTSModelMultiAcc_v3", language: str):
        if "random" in model.speakers:
            model.speakers.remove("random")

        self.speakers[language] = model.speakers
        for speaker in model.speakers:
            self.model_by_speaker[speaker] = model
    
    def _delete_dashes(self, text: str) -> str:
        # This fixes the problem:
        # https://github.com/twirapp/silero-tts-api-server/issues/8
        return text.replace("-", "").replace("‑", "")

    def _generate_audio(
        self, model: "TTSModelMultiAcc_v3", text: str, speaker: str, sample_rate: int
    ) -> bytes:
        try:
            audio: torch.Tensor = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate)
        except ValueError:
            raise NotCorrectTextException(text)
        except Exception as error:
            if str(error) == "Model couldn't generate your text, probably it's too long":
                raise TextTooLongException(text)
            raise
        else:
            return self._convert_to_wav(model, audio, sample_rate)

    def _convert_to_wav(self, model: "TTSModelMultiAcc_v3", audio: torch.Tensor, sample_rate: int) -> bytes:
        with BytesIO() as buffer:
            model.write_wave(
                buffer,
                audio=self._normalize_audio(audio),
                sample_rate=sample_rate,
            )
            buffer.seek(0)
            return buffer.read()

    def _normalize_audio(self, audio: torch.Tensor):
        audio: np.ndarray = audio.numpy() * MAX_INT16
        return audio.astype(np.int16)

tts = TTS()
