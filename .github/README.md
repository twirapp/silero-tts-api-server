> [!NOTE]
> I'm using python version 3.9 for development, this should work on all 3 versions

# Installation
1. Clone the repository
    ```bash
    git clone https://github.com/gigachad-dev/silero-tts-api-server.git && cd silero-tts-api-server
    ```
2. Create virtual environment and activate it
    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```
3. Install dependencies
    ```bash
    pip3 install -r requirements.txt
    ```

# Run http server
```bash
python3 server.py
```
The default will be [localhost:8000](http://localhost:8000/docs)

All endpoints can be viewed and tested at [localhost:8000/docs](http://localhost:8000/docs)