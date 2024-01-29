from dotenv import load_dotenv
import sentry_sdk


def run_server():
    import uvicorn

    uvicorn.run("server:app", host="localhost", port=8000)

load_dotenv()
sentry_sdk.init()

if __name__ == "__main__":
    run_server()
else:
    # this is needed to start the server via the uvicorn command
    from server import app
