FROM python:3.9-slim

# Set environment variables for better logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV FLASK_ENV=production

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Debug: List all files to verify model is copied
RUN echo "\n=== CONTAINER FILE STRUCTURE ===" && \
    echo "\n=== Files in /app ===" && \
    ls -la /app/ && \
    echo "\n=== Files in /app/utils ===" && \
    ls -la /app/utils/ || echo "utils directory not found" && \
    echo "\n=== Looking for .pkl files ===" && \
    find /app -name "*.pkl" -o -name "*.pkl.gz" | xargs ls -la || echo "No .pkl files found" && \
    echo "\n=== File sizes ===" && \
    du -sh /app/* 2>/dev/null || true

# Set permissions
RUN chmod -R 755 /app
RUN chmod 644 /app/phishing_model.pkl 2>/dev/null || echo "Model file not found for chmod"

# Expose port
EXPOSE 10000

# Run the application with unbuffered output
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000", "--workers", "2", "--timeout", "120", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-"]
