# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /workspace

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Install Vite globally
RUN npm install -g vite

# Copy the rest of your application code
COPY . .

# Expose ports for Django and Redis
EXPOSE 8000
EXPOSE 6379

# Command to run your application
CMD ["sh", "-c", "daphne simulateur.asgi:application --port 8000 --bind"]
