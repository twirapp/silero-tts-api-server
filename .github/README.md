<!-- Created in https://leviarista.github.io/github-profile-header-generator/ -->
![Header](./header.png)

# Languages supported

> [!NOTE]
> All models are from the repository: [snakers4/silero-models](https://github.com/snakers4/silero-models)

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

# Installation via docker

> [!IMPORTANT]
> This requires [docker](https://www.docker.com/products/docker-desktop/) installed and the docker daemon running
```bash
docker run --rm -p 8000:8000 twirapp/silero-tts-api-server
```

<details>
<summary>Build and run from local repository</summary>

Clone the repository:
```bash
git clone https://github.com/twirapp/silero-tts-api-server.git && cd silero-tts-api-server
```

Build docker image:
```bash
docker build -f docker/Dockerfile -t silero-tts-api-server .
```

Run the container:
```bash
docker run --rm -p 8000:8000 silero-tts-api-server
```

Or use docker compose:
```bash
docker-compose -f docker/compose.yml up
```

</details>

# Installation

> [!IMPORTANT]
> Minimum requirement [python 3.9](https://www.python.org/downloads/)
>
> This project uses [rye](https://rye-up.com) for dependency management, it assumes you have installed it

1. Clone the repository
    ```bash
    git clone https://github.com/twirapp/silero-tts-api-server.git && cd silero-tts-api-server
    ```
2. Install dependencies

    This will automatically create the virtual environment in the `.venv` directory and install the required dependencies
    ```bash
    rye sync
    ```
    <details>
    <summary>(not recommended) alternative install via pip</summary>
    Create a virtual environment and activate

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```
    Remove line 10 `-e file:.` from the `requirements.lock` file and then run the command
    ```bash
    pip3 install -r requirements.lock
    ```
    </details>
3. Download silero tts models
    ```bash
    bash ./install_models.sh
    ```
4. Run the server
    ```bash
    litestar run
    ```
> [!NOTE]
> The default will be [localhost:8000](http://localhost:8000/)

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

- `GET` `/generate` - Generate audio in wav format from text. Parameters: `text` `speaker` `sample_rate`
- `GET` `/speakers` - Get list of speakers

# Environment variables

- `TEXT_LENGTH_LIMIT` - Maximum length of the text to be processed. Default is 930 characters.
- `MKL_NUM_THREADS` - Number of threads to use for generating audio. Default number of threads: number of CPU cores.

# Considerations for the future

This repository is dedicated to twir.app and is designed to meet its requirements.

TwirApp needs to generate audio using the CPU. If support for other devices such as cuda or mps is needed, please [open an issue](https://github.com/twirapp/silero-tts-api-server/issues/new?title=Support%20for%20%60cuba%60%20and%20%60mps%60%20devices).
