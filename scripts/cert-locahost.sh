#!/bin/bash

# Generate a self-signed SSL certificate for localhost
echo "Generating SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt -subj "/CN=localhost"

# Change directory to your project folder
echo "Navigating to project directory..."
cd ../simulateur || { echo "Directory 'simulateur' not found. Exiting."; exit 1; }

# Start Daphne with SSL enabled
echo "Starting Daphne with SSL..."
python3 -m daphne -e ssl:8001:privateKey=localhost.key:certKey=localhost.crt simulateur.asgi:application --bind 0.0.0.0 &

# Allow some time for the server to start
sleep 5

# Test the HTTPS connection using curl
echo "Testing HTTPS connection..."
curl -k https://localhost:8000

# Print instructions to the user
echo "To stop Daphne, use 'kill $!' or 'pkill -f daphne'."
