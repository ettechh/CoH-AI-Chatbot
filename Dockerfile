# Dockerfile for CoH-AI Chatbot
# Use official Python 3.11 slim image
FROM python:3.11.5-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure stdout/stderr are flushed immediately
ENV PYTHONUNBUFFERED 1

# ----------------------
# Install system dependencies
# ----------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ----------------------
# Copy application files
# ----------------------
COPY . /app

# ----------------------
# Install Python dependencies
# ----------------------
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------
# Expose Flask default port
# ----------------------
EXPOSE 5000

# ----------------------
# Set environment variables for Flask
# ----------------------
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# ----------------------
# Run the app
# ----------------------
CMD ["flask", "run"]
