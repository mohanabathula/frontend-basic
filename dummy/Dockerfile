# Use an official Python runtime as a parent image
FROM ubuntu:20.04

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Upgrade pip
# RUN python3 -m pip install --no-cache-dir --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY dum.py .
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 30010

# Run app.py when the container launches
CMD ["python3", "dum.py"]
