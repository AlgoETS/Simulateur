# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /workspace

# Install GCC, PostgreSQL client, and other necessary build tools
RUN apt-get update && \
    apt-get install -y gcc build-essential postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --use-feature=fast-deps -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the environment variable for Django settings module
ENV DJANGO_SETTINGS_MODULE=simulateur.settings

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the application
EXPOSE 8000

# Start the application
CMD ["./run.sh"]
