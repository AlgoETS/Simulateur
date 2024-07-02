# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /workspace

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Copy the rest of your application code
COPY . .

# Expose ports for Django and Redis
EXPOSE 8000
EXPOSE 6379

# Command to run your application
CMD ["sh", "-c", "daphne simulateur.asgi:application -b 0.0.0.0 -p 8000"]
