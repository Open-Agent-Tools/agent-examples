#!/bin/sh
set -e

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
until curl -s http://ollama:11434/api/tags >/dev/null; do
  sleep 1
done

echo "Ollama is ready. Loading models..."

# List of models to pull - modify this list as needed
MODELS="llama4:latest gemma3:27b gemma3:4b gemma3:1b gemma3n:latest"

# Pull each model
for MODEL in $MODELS; do
  curl -X POST http://ollama:11434/api/pull -d "{\"name\":\"$MODEL\"}"
  echo "Model $MODEL pulled successfully"
done

echo "All models loaded successfully"
