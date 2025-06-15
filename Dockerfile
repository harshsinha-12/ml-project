# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire application code first
COPY . .

# Create a temporary requirements file without -e .
RUN grep -v -- "-e \." requirements.txt > requirements_docker.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements_docker.txt

# Install the local package in development mode
RUN pip install -e .

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the application when the container launches
CMD ["python", "application.py"]
