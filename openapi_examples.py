from fastapi import Query

TextExamples = Query(
    openapi_examples={
        "ru_1": {
            "value": "Съешьте ещё этих мягких французских булочек, да выпейте чаю."
        },
        "ru_2": {
            "value": "В недрах тундры выдры в гетрах тырят в вёдра ядра кедров."
        },
        "en_1": {
            "value": "Can you can a canned can into an un-canned can like a canner can can a canned can into an un-canned can?"
        },
    }
)

SpeakerExamples = Query(
    openapi_examples={
        "ru_aidar": {"value": "aidar"},
        "ru_baya": {"value": "baya"},
        "en_0": {"value": "en_0"},
    }
)

SampleRateExamples = Query(
    openapi_examples={
        "8 000": {"value": 8_000},
        "24 000": {"value": 24_000},
        "48 000": {"value": 48_000},
    }
)
