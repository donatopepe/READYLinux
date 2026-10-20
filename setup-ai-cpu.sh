#!/usr/bin/env bash
# Opt-in installer. Internet needed ONLY now, never for inference.
set -euo pipefail
AI_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/readylinux/ai"
SRC_DIR="$AI_DIR/llama.cpp"
MODEL_DIR="$AI_DIR/models"
MODEL="$MODEL_DIR/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
MODEL_URL='https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf'
MODEL_SHA='cc324af070c2ecbfd324a30884d2f951a7ff756aba85cb811a6ec436933bb046'
for tool in git cmake curl sha256sum c++; do
  command -v "$tool" >/dev/null 2>&1 || { echo "Manca: $tool" >&2; exit 1; }
done
printf '%s\n' 'READY Linux: installazione IA locale CPU-only (opt-in)' \
  'Scarichera llama.cpp da GitHub e circa 1,12 GB di modello GGUF da Hugging Face.' \
  "Destinazione: $AI_DIR" \
  'Non installa servizi di sistema, non usa sudo e non abilita alcuna API cloud.'
mkdir -p -- "$AI_DIR" "$MODEL_DIR"
if [ ! -d "$SRC_DIR/.git" ]; then
  if [ -e "$SRC_DIR" ]; then
    echo "Percorso esistente non gestito da Git: $SRC_DIR" >&2
    exit 1
  fi
  git clone --depth 1 https://github.com/ggml-org/llama.cpp.git "$SRC_DIR"
else
  echo "Sorgenti llama.cpp gia' presenti: nessun aggiornamento automatico."
fi
# Explicitly CPU-only: no CUDA/Metal/Vulkan backend compiled.
cmake -S "$SRC_DIR" -B "$SRC_DIR/build" -DGGML_CUDA=OFF -DGGML_METAL=OFF -DGGML_VULKAN=OFF -DCMAKE_BUILD_TYPE=Release
cmake --build "$SRC_DIR/build" --config Release -j "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)" --target llama-server
if [ -f "$MODEL" ]; then
  echo 'Modello gia presente: verifica SHA-256.'
  echo "$MODEL_SHA  $MODEL" | sha256sum -c - || { echo 'Modello esistente non verificato: non sovrascrivo.' >&2; exit 1; }
else
  tmp="$MODEL_DIR/.download-$$.gguf"
  trap 'rm -f -- "$tmp"' EXIT
  curl --fail --location --retry 2 --output "$tmp" "$MODEL_URL"
  echo "$MODEL_SHA  $tmp" | sha256sum -c - || { echo 'SHA-256 non corrisponde: download rifiutato.' >&2; exit 1; }
  mv -- "$tmp" "$MODEL"
  trap - EXIT
fi
printf '\nInstallazione completata.\n  Binario: %s\n  Modello: %s\n\n' "$SRC_DIR/build/bin/llama-server" "$MODEL"
echo 'Ora avvia READY Linux e digita: AI START; poi AI STATUS; poi AI ASK ...'
