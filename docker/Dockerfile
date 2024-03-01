FROM python:3.12.2-slim-bookworm as base
LABEL org.opencontainers.image.authors="MrPandir <MrPandir@users.noreply.github.com>"
LABEL org.opencontainers.image.source="https://github.com/twirapp/silero-tts-api-server"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="Silero TTS API server"
LABEL org.opencontainers.image.description="This is a simple server that uses Silero models to convert text to audio files over HTTP"
LABEL org.opencontainers.image.vendor="TwirApp"

FROM base as dependencies-installer
WORKDIR /app
SHELL ["/bin/bash", "-c"]
RUN apt-get -y update && apt-get -y install curl && \
    apt-get autoremove && apt-get clean
# disabling uv is a temporary solution until this is fixed:
# https://github.com/astral-sh/uv/issues/1497
# And also until rye updates uv to the latest versions, at the time of writing rye is using version 0.1.0
RUN curl -sSf https://rye-up.com/get | NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" RYE_TOOLCHAIN=/usr/local/bin/python3 bash && \
    bash -c "source $HOME/.rye/env && rye pin 3.12.2 && rye config --set-bool behavior.use-uv=false"
ENV PATH=/root/.rye/shims:$PATH
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache rye sync --no-dev

FROM base as models-installer
RUN apt-get -y update && apt-get -y install curl
COPY models models
COPY install_models.sh install_models.sh
RUN chmod -x install_models.sh && bash ./install_models.sh >&2

FROM base
WORKDIR /app
COPY --from=models-installer /models /app/models
COPY --from=dependencies-installer /app/.venv .venv
ENV PATH=/app/.venv/bin:$PATH
COPY /app ./app
COPY /tts ./tts
CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]
