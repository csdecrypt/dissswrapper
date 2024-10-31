    # Use an official Python runtime as a parent image
    FROM python:3.10-slim

    # Set a working directory inside the container
    WORKDIR /app

    # Install system dependencies (e.g., ffmpeg)
    RUN apt-get update && apt-get install -y \
        ffmpeg \
        && rm -rf /var/lib/apt/lists/*

    #required?
    RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

    # Copy requirements.txt first to leverage Docker caching
    # removed datasets[audio]==2.17.0
    COPY requirements.txt .

    # Install Python dependencies
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy openai/whisper-large-v3 model
    COPY whisper_large_model ./whisper_large_model

    # Copy the Flask application into the container
    COPY app.py .

    # Command to run your Flask application
    CMD ["python", "app.py"]

    # Expose the port for the Flask application
    EXPOSE 5000
