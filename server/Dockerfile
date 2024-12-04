# Base image
#FROM ubuntu:latest
FROM ultralytics/yolov5:latest
# Set the working directory in the container
WORKDIR /app

RUN apt update && apt install python3-pip -y && apt install ffmpeg -y

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code and yolo model into the container 
COPY yolov5s.pt .
COPY ser.py .

EXPOSE 30020

# Start the server
CMD ["python3", "ser.py"]
