FROM python:3.12.2-slim-bookworm as base
LABEL org.opencontainers.image.authors="MrPandir <MrPandir@users.noreply.github.com>"
LABEL org.opencontainers.image.source="https://github.com/twirapp/silero-tts-api-server"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="Silero TTS API server"
LABEL org.opencontainers.image.description="This is a simple server that uses Silero models to convert text to audio files over HTTP"
LABEL org.opencontainers.image.vendor="TwirApp"

# Install all dependencies from requirements.lock
FROM base as dependencies-installer
WORKDIR /app
RUN <<EOF
    apt-get -y update && apt-get -y install curl
    apt-get autoremove && apt-get clean
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ln -s /root/.cargo/bin/uv /usr/local/bin/uv
    uv venv
EOF
COPY requirements.lock .
RUN --mount=type=cache,target=/root/.cache uv pip install --no-deps -r requirements.lock

# Install all silero models from the Internet or locally if available in the `models` directory
FROM base as models-installer
RUN apt-get -y update && apt-get -y install curl
COPY models models
COPY install_models.sh install_models.sh
RUN chmod -x install_models.sh && bash ./install_models.sh >&2


FROM base
WORKDIR /app
COPY --from=models-installer /models models
COPY --from=dependencies-installer /app/.venv .venv
ENV PATH=/app/.venv/bin:$PATH
COPY ./app app
COPY ./tts tts
CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]
