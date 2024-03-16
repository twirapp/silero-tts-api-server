[![Banner](.github/banner.png)](https://github.com/TwirApp/silero-tts-api-server)

[Github Repository](https://github.com/TwirApp/silero-tts-api-server)

# Languages supported

All models are from the repository: [snakers4/silero-models](https://github.com/snakers4/silero-models)

| Language | Model | Speakers |
|--------|--------|--------|
| Russian | v4_ru | 5: aidar, baya, kseniya, xenia, eugene |
| Ukrainian | v4_ua | 1: mykyta |
| Uzbek | v4_uz | 1: dilnavoz | 
| English | v3_en | 118: en_0, en_1, ..., en_117 |
| Spanish | v3_es | 3: es_0, es_1, es_2 |
| French | v3_fr | 6: fr_0, fr_1, fr_2, fr_3, fr_4, fr_5 | 
| German | v3_de | 5: bernd_ungerer, eva_k, friedrich, hokuspokus, karlsson | 
| Tatar | v3_tt | 1: dilyara | 
| Mongolian | v3_xal | 2: erdni, delghir | 

# Launch a docker container

```bash
docker run --rm -p 8000:8000 twirapp/silero-tts-api-server
```

# Example of use via docker compose

```yml
version: '3'
services:
    silero-tts-api-server:
        image: twirapp/silero-tts-api-server
        ports:
            - "8000:8000"
        environment:
            - TEXT_LENGTH_LIMIT=930
            - MKL_NUM_THREADS=8
```

# Documentation

You can view the automatically generated documentation based on OpenAPI at:

| Provider | Url |
|--------|--------|
| [Swagger](https://swagger.io) | https://localhost:8000/schema/ |
| [ReDoc](https://redocly.com/redoc) | https://localhost:8000/schema/redoc |
| [Stoplight Elements](https://stoplight-site.webflow.io/open-source/elements) | https://localhost:8000/schema/elements |
| [RepiDoc](https://rapidocweb.com) | https://localhost:8000/schema/repidoc |
| OpenAPI schema yaml | https://localhost:8000/schema/openapi.yaml |
| OpenAPI schema json | https://localhost:8000/schema/openapi.json |

# Endpoints

- `GET` `/generate` - Generate audio in wav format from text. Parameters: `text` `speaker` `sample_rate`, `pitch`, `rate`
- `GET` `/speakers` - Get list of speakers

`sample_rate` can be set from 8 000, 24 000, 48 000
`pitch` and `rate` can be set from 0 to 100

# Environment variables

- `TEXT_LENGTH_LIMIT` - Maximum length of the text to be processed. Default is 930 characters.
- `MKL_NUM_THREADS` - Number of threads to use for generating audio. Default number of threads: number of CPU cores.

# Considerations for the future

This repository is dedicated to twir.app and is designed to meet its requirements.

TwirApp needs to generate audio using the CPU. If support for other devices such as cuda or mps is needed, please [open an issue](https://github.com/twirapp/silero-tts-api-server/issues/new?title=Support%20for%20%60cuba%60%20and%20%60mps%60%20devices).
