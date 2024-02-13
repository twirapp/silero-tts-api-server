from os import environ
from typing import Annotated

from dotenv import load_dotenv
from litestar import Litestar, get, Response
from litestar.openapi import OpenAPIConfig
from litestar.config.response_cache import CACHE_FOREVER
from litestar.params import Parameter

from tts import tts
from openapi_examples import *
from http_exceptions import *
from exceptions import *


load_dotenv()

SILERO_MAX_TEXT_LENGTH = 930
text_length_limit = min(
    int(environ.get("TEXT_LENGTH_LIMIT", SILERO_MAX_TEXT_LENGTH)),
    SILERO_MAX_TEXT_LENGTH,
)


@get(
    "/generate",
    summary="Generate WAV audio from text",
    media_type="audio/wav",
    sync_to_thread=True,
    raises=genetate_exceptions,
)
def generate(
    text: Annotated[str, Parameter(examples=text_examples)],
    speaker: Annotated[str, Parameter(examples=speaker_examples)],
    sample_rate: Annotated[
        int, Parameter(examples=sample_rate_examples, default=48_000)
    ],
) -> Response:
    if len(text) > text_length_limit:
        raise TextTooLongHTTPException(
            {"text": text, "length": len(text), "max_length": text_length_limit}
        )

    try:
        audio = tts.generate(text, speaker, sample_rate)
    except NotFoundModelException:
        raise NotFoundSpeakerHTTPException({"speaker": speaker})
    except NotCorrectTextException:
        raise NotCorrectTextHTTPException({"text": text})
    except TextTooLongException:
        raise TextTooLongHTTPException(
            {"text": text, "length": len(text), "max_length": text_length_limit}
        )
    except InvalidSampleRateException:
        raise InvalidSampleRateHTTPException(
            {"sample_rate": sample_rate, "valid_sample_rates": tts.VALID_SAMPLE_RATES}
        )
    else:
        return Response(audio, media_type="audio/wav")


@get("/speakers", summary="List available speakers", cache=CACHE_FOREVER)
async def speakers() -> dict[str, list[str]]:
    return tts.speakers


app = Litestar(
    [generate, speakers],
    openapi_config=OpenAPIConfig(title="Silero TTS API", version="1.0.0"),
)
