from typing import Annotated

from fastapi import FastAPI, Response, HTTPException, status

from tts import tts
from openapi_examples import TextExamples, SpeakerExamples, SampleRateExamples
from openapi_responses import GENERATE_RESPONSES
from exceptions import NotFoundModelException, NotCorrectTextException

app = FastAPI()


@app.get("/generate", responses=GENERATE_RESPONSES)
def generate(
    text: Annotated[str, TextExamples],
    speaker: Annotated[str, SpeakerExamples],
    sample_rate: Annotated[int, SampleRateExamples] = 48_000,
):
    if sample_rate not in (8_000, 24_000, 48_000):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Invalid sample rate: {sample_rate}. Use 8 000, 24 000 or 48 000")
    try:
        audio = tts.generate(text, speaker, sample_rate)
    except NotFoundModelException as error:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail=str(error))
    except NotCorrectTextException as error:
        return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))
    else:
        return Response(audio, media_type="audio/wav")


@app.get("/speakers")
def speakers():
    return tts.speakers


if __name__ == "__main__":
    import uvicorn
    import sentry_sdk
    from dotenv import load_dotenv

    load_dotenv()
    sentry_sdk.init()

    uvicorn.run(app, host="localhost", port=8000)
