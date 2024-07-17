# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /workspace

# Install GCC and other necessary build tools
RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run collectstatic and migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port 8000 for the application
EXPOSE 8000

# Start the application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "simulateur.asgi:application"]
