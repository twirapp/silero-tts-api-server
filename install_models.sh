#!/bin/bash

modelUrls=(
"https://models.silero.ai/models/tts/de/v3_de.pt"
"https://models.silero.ai/models/tts/en/v3_en.pt"
"https://models.silero.ai/models/tts/es/v3_es.pt"
"https://models.silero.ai/models/tts/fr/v3_fr.pt"
"https://models.silero.ai/models/tts/tt/v3_tt.pt"
"https://models.silero.ai/models/tts/xal/v3_xal.pt"
"https://models.silero.ai/models/tts/ru/v4_ru.pt"
"https://models.silero.ai/models/tts/ua/v4_ua.pt"
"https://models.silero.ai/models/tts/uz/v4_uz.pt"
)

if [ ! -d "models" ]; then
  mkdir models
fi

cd models

download_model() {
  modelUrl="$1"
  echo "Starting download: $modelUrl"
  if curl -fSL -O "$modelUrl" --progress-bar -A "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"; then
    echo "Completed download: $(basename "$modelUrl")"
  else
    echo "Failed download: $(basename "$modelUrl")"
    exit 1
  fi
}

for modelUrl in "${modelUrls[@]}"; do
  download_model "$modelUrl"
done

echo "All downloads have been processed."
