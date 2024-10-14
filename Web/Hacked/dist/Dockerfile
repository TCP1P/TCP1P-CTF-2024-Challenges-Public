# Use the official Python image as the base image
FROM python:3.8-slim

# Set environment variables for Flask
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy and move flag
COPY flag.txt /app/
RUN mv flag.txt /$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1).txt

# Copy source code
COPY application /app/

# Expose the port that the app will run on
EXPOSE 1337

# Start the Flask application
CMD ["python", "app.py"]
