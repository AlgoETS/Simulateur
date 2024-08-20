#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

# Use the first argument passed to the script as the model name, or default to 'llama3'.
MODEL_NAME=${1:-llama3}

echo "🔴 Retrieving model: $MODEL_NAME..."
ollama pull $MODEL_NAME
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
