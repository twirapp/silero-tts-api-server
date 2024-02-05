from dotenv import load_dotenv


def run_server():
    import uvicorn

    uvicorn.run("server:app", host="localhost", port=8000)

load_dotenv()

if __name__ == "__main__":
    run_server()
else:
    # this is needed to start the server via the uvicorn command
    from server import app
