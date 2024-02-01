FROM python:3.9-slim as base

FROM base as pip-installer
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --user -r requirements.txt

FROM base as models-installer
WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY install_models.sh install_models.sh
RUN chmod -x install_models.sh && bash ./install_models.sh >&2


FROM base
WORKDIR /app

COPY . /app
COPY --from=models-installer /app/models /app/models
COPY --from=pip-installer /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
