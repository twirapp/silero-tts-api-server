FROM python:3.9-slim as base

FROM base as models-installer
WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY install_models.sh install_models.sh
RUN chmod -x install_models.sh && bash ./install_models.sh >&2


FROM base
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
COPY --from=models-installer /app/models /app/models

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
