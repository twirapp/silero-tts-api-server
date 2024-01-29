from typing import TYPE_CHECKING
from pathlib import Path

import torch
from torch.package import PackageImporter

from io import BytesIO
from exceptions import NotFoundModelException, NotCorrectTextException

if TYPE_CHECKING:
    from .typing.package import TTSModelMultiAcc_v3


# fixes import package error on Mac
# https://github.com/snakers4/silero-models/discussions/104
torch.backends.quantized.engine = "qnnpack"

print(f"Using {torch.get_num_threads()} threads. To change, set environment variable MKL_NUM_THREADS")

device = torch.device("cpu")


class TTS:
    def __init__(self):
        self.models: dict[str, "TTSModelMultiAcc_v3"] = {}
        self.speakers: dict[str, list[str]] = {}
        self.model_by_speaker: dict[str, "TTSModelMultiAcc_v3"] = {}

        for model_path in Path("models").glob("*.pt"):
            self._load_model(model_path)

    def generate(self, text: str, speaker: str, sample_rate: int) -> bytes:
        model = self.model_by_speaker.get(speaker)
        if model is None:
            raise NotFoundModelException(speaker)

        return self._generate_audio(model, text, speaker, sample_rate)

    def _load_model(self, model_path: Path):
        package = PackageImporter(model_path)
        model: "TTSModelMultiAcc_v3" = package.load_pickle("tts_models", "model")
        model.to(device)

        language = model_path.stem[3:]
        self.models.update({language: model})

        self._load_speakers(model, language)

    def _load_speakers(self, model: "TTSModelMultiAcc_v3", language: str):
        if "random" in model.speakers:
            model.speakers.remove("random")

        self.speakers.update({language: model.speakers})
        for speaker in model.speakers:
            self.model_by_speaker[speaker] = model

    def _generate_audio(
        self, model: "TTSModelMultiAcc_v3", text: str, speaker: str, sample_rate: int
    ) -> bytes:
        try:
            audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate)
        except ValueError:
            raise NotCorrectTextException(text)

        buffer = BytesIO()
        model.write_wave(
            buffer,
            audio=(audio * 32767).numpy().astype("int16"),
            sample_rate=sample_rate,
        )
        buffer.seek(0)

        return buffer.read()


tts = TTS()
