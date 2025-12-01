# Use the latest stable Python 3.13 slim image
FROM python:3.13-slim

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# FIX: Set library path for native dependencies (like libgl)
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
# --no-cache-dir is good practice
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (Cloud Run uses 8080 by default)
ENV PORT 8080

# FIX: Use a safer ENTRYPOINT format to guarantee Gunicorn runs correctly
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]