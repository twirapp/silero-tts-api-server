<!-- Created in https://leviarista.github.io/github-profile-header-generator/ -->
![Header](./header.png)

## Languages supported

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

# Installation
> [!IMPORTANT]
> Minimum requirement python 3.9

> [!NOTE]
> I'm using python version 3.9.6 for development

1. Clone the repository
    ```bash
    git clone https://github.com/gigachad-dev/silero-tts-api-server.git && cd silero-tts-api-server
    ```
2. (Recommended) Create virtual environment and activate it
    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```
3. Install dependencies
    ```bash
    pip3 install -r requirements.txt
    ```

# Run API server
```bash
python3 server.py
```
> [!NOTE]
>  The default will be [localhost:8000](http://localhost:8000/docs). All endpoints can be viewed and tested at [localhost:8000/docs](http://localhost:8000/docs)

# Run API server via docker
```bash
docker run --rm -p 8000:8000 twirapp/silero-tts-api-server
```

<details>
<summary>Advanced</summary>

Build the API server image:
```bash
docker build --rm -f docker/Dockerfile -t silero-tts-api-server .
```

Run the API server container:
```bash
docker run --rm -p 8000:8000 silero-tts-api-server
```

Run the Docker Compose to start the server:
```bash
docker-compose -f docker/docker-compose.yml up
```

</details>