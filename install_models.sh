#!/bin/bash

models=(
  "2e22f38619e1d1da96d963bda5fab6d53843e8837438cb5a45dc376882b0354b https://models.silero.ai/models/tts/de/v3_de.pt"
  "02b71034d9f13bc4001195017bac9db1c6bb6115e03fea52983e8abcff13b665 https://models.silero.ai/models/tts/en/v3_en.pt"
  "36206add75fb89d0be16d5ce306ba7a896c6fa88bab7e3247403f4f4a520eced https://models.silero.ai/models/tts/es/v3_es.pt"
  "02ed062cfff1c7097324929ca05c455a25d4f610fd14d51b89483126e50f15cb https://models.silero.ai/models/tts/fr/v3_fr.pt"
  "368c8f55e6de1b54dc5a393f0f5bcd328f84b3d544ac6f8b9654fc23730e925d https://models.silero.ai/models/tts/tt/v3_tt.pt"
  "fcababc14c6dbbffb14d04e490e4d2d85087f4aa42b2ae9d33f147cd4b868b76 https://models.silero.ai/models/tts/xal/v3_xal.pt"
  "896ab96347d5bd781ab97959d4fd6885620e5aab52405d3445626eb7c1414b00 https://models.silero.ai/models/tts/ru/v4_ru.pt"
  "ee14ace1b9ef79ab6af53cf14fdba17d80de209ee6c34dc69efc65a5a5458165 https://models.silero.ai/models/tts/ua/v4_ua.pt"
  "46c7977beccf2f3c9f730de281f8efefe60ee8f293a2047e89aebe567b3ed4d7 https://models.silero.ai/models/tts/uz/v4_uz.pt"
)

if [ ! -d "models" ]; then
  mkdir models
fi

cd models

verify_hash() {
  local file="$1"
  local expectedHash="$2"
  local currentHash

  if command -v sha256sum >/dev/null 2>&1; then
    currentHash=$(sha256sum "$file" | cut -d ' ' -f 1)
  elif command -v shasum >/dev/null 2>&1; then
    currentHash=$(shasum -a 256 "$file" | cut -d ' ' -f 1)
  else
    return 1
  fi
}

download_model() {
  local modelUrl="$1"

  echo "Starting download: $modelUrl"
  if curl -fSL -O "$modelUrl" --progress-bar -A "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"; then
    echo "Completed download: $(basename "$modelUrl")"
  else
    echo "Failed download: $(basename "$modelUrl")"
    exit 1
  fi
}

for model in "${models[@]}"; do
  modelUrl="${model##* }"
  modelHash="${model%% *}"
  modelFile="$(basename "$modelUrl")"

  if [ -f "$modelFile" ] && verify_hash "$modelFile" "$modelHash"; then
    echo "Model $modelFile already exists and has the correct hash, skipping download."
  else
    download_model "$modelUrl"
  fi
done

echo "All downloads have been processed."
