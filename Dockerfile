# Use official Python runtime as a parent image
FROM python:3.10-slim

RUN apt update -y
RUN apt-get update
RUN apt-get install -y build-essential libportaudio2 portaudio19-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Define environment variable to ensure output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]

