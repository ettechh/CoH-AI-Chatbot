# Use the same Python version as your local environment
FROM python:3.11.5-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install system dependencies required for MySQL + builds
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask default port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "main.py"]
