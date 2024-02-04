GENERATE_RESPONSES = {
    200: {"content": {"audio/wav": {}}},
    404: {
        "content": {
            "application/json": {
                "example": {
                    "status_code": 404,
                    "detail": "Model not found for speaker: {speaker_name}",
                }
            }
        },
        "description": "Model not found for speaker",
    },
    400: {
        "content": {
            "application/json": {
                "example": {
                    "status_code": 400,
                    "detail": "Invalid sample rate: {sample_rate}. Use 8 000, 24 000 or 48 000",
                }
            }
        },
        "description": "Invalid sample rate",
    },
    422: {
        "content": {
            "application/json": {
                "example": {
                    "status_code": 422,
                    "detail": "Text not correct: {text}",
                }
            }
        },
        "description": "Text not correct",
    },
    413: {
        "content": {
            "application/json": {
                "example": {
                    "status_code": 413,
                    "detail": "Text too long. Length is {len(text)}. Max length is 930 symbols.",
                }
            }
        },
        "description": "Text too long",
    },
}

