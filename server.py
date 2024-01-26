from typing import Annotated

from fastapi import FastAPI, Response

from tts import tts
from openapi_examples import TextExamples, SpeakerExamples, SampleRateExamples


app = FastAPI()


@app.get("/generate")
def generate(
    text: Annotated[str, TextExamples],
    speaker: Annotated[str, SpeakerExamples],
    sample_rate: Annotated[int, SampleRateExamples] = 48_000,
):
    audio = tts.generate(text, speaker, sample_rate)
    return Response(audio, media_type="audio/wav")


@app.get("/speakers")
def speakers():
    return tts.speakers


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
