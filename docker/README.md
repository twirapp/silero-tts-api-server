<!-- Created in https://leviarista.github.io/github-profile-header-generator/ -->
![Header](.github/header.png)

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

All languages support sample rate: 8 000, 24 000, 48 000

# How to use this image
```bash
docker run --rm -p 8000:8000 twirapp/silero-tts-api-server
```

## Here is an example using docker-compose.yml:
```yml
version: '3'
services:
    app:
        image: twirapp/silero-tts-api-server
        ports:
            - "8000:8000"
        environment:
            - TEXT_LENGTH_LIMIT=930
            - MKL_NUM_THREADS=8
```

## Environment variables:

- TEXT_LENGTH_LIMIT: Maximum length of the text to be processed. Default is 930 characters.
- MKL_NUM_THREADS: Number of threads to use for generating audio. Default number of threads: number of CPU cores.
