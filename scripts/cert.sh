#!/bin/bash

# Install OpenSSL if not already installed (Debian-based systems)
sudo apt update
sudo apt install -y openssl

# Generate the private key
openssl genpkey -algorithm RSA -out key.pem -aes256

# sleep for 1 second to allow the user to enter the password
sleep 1

# Generate the CSR
openssl req -new -key key.pem -out csr.pem

# sleep for 1 second to allow the user to enter the password
sleep 1

# Generate the self-signed certificate
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out crt.pem

# sleep for 1 second to allow the user to enter the password
sleep 1

# Run daphne with SSL
cd simulateur

mv ../key.pem . && mv ../crt.pem .
sudo daphne -e ssl:443:privateKey=key.pem:certKey=crt.pem simulateur.asgi:application
