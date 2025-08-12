#!/bin/sh

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
until curl -s http://ollama:11434/api/tags >/dev/null; do
  sleep 1
done

echo "Ollama is ready. Loading models..."

# List of models to pull - modify this list as needed
MODELS="gemma3:4b gemma3n:latest"

# Pull each model
for MODEL in $MODELS; do
  if curl -X POST http://ollama:11434/api/pull -d "{\"name\":\"$MODEL\"}"; then
    echo "Model $MODEL pulled successfully"
  else
    echo "Failed to pull model $MODEL"
    exit 1
  fi
done

echo "All models loaded successfully"