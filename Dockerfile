# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make main.py executable
RUN chmod +x main.py

# Create a non-root user
RUN useradd --create-home --shell /bin/bash trader
RUN chown -R trader:trader /app
USER trader

# Expose port (if needed for future web interface)
EXPOSE 8000

# Default command
CMD ["python", "main.py"]
