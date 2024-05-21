FROM python:3.11-slim-bookworm as base
LABEL org.opencontainers.image.authors="MrPandir <MrPandir@users.noreply.github.com>"
LABEL org.opencontainers.image.source="https://github.com/twirapp/silero-tts-api-server"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="Silero TTS API server"
LABEL org.opencontainers.image.description="This is a simple server that uses Silero models to convert text to audio files over HTTP"
LABEL org.opencontainers.image.vendor="TwirApp"

# Install all dependencies from pyproject.toml
# NOTE: Rye is used because you need to determine which version of torch to use +cpu or not
# NOTE: The problem with uv is that it does not read the rye.excluded-dependencies metadata
FROM base as dependencies-installer
WORKDIR /app
RUN <<EOF
    apt-get -y update && apt-get -y install curl
    apt-get autoremove && apt-get clean

    curl -LsSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" RYE_TOOLCHAIN=/usr/local/bin/python3 bash
    ln -s /root/.rye/shims/rye /usr/local/bin/rye
    rye pin 3.11
    rye config --set-bool behavior.use-uv=true
EOF
COPY pyproject.toml .
RUN --mount=type=cache,target=/root/.cache rye sync --no-dev

# Install all silero models from the Internet or locally if available in the `models` directory
FROM base as models-installer
RUN apt-get -y update && apt-get -y install curl
COPY models models
COPY install_models.sh install_models.sh
RUN chmod -x ./install_models.sh && bash ./install_models.sh >&2

# Distroless is a small image with only python, providing a non-root user
FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app
ENV PATH=/app/.venv/bin:$PATH
# This is necessary for Python to understand where to look for libraries.
ENV PYTHONPATH="/app/.venv/lib/python3.11/site-packages/:$PYTHONPATH"
USER nonroot
COPY --from=models-installer /models models
COPY --from=dependencies-installer /app/.venv .venv
COPY ./app app
COPY ./tts tts
CMD ["/app/.venv/bin/litestar", "run", "--host", "0.0.0.0", "--port", "8000"]
