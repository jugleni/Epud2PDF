# Use official Python base image
FROM python:3.10-slim

# Install system dependencies required for WeasyPrint
RUN apt-get update && \
    apt-get install -y build-essential libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy dependency files to container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to container
COPY app.py .

# Expose Flask port
EXPOSE 3453

# Command to run the application
CMD ["python", "-u", "app.py"]