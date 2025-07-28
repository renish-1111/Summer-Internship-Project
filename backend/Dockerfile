# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app/backend

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpoppler-cpp-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Copy requirements and install Python dependencies with uv
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# Copy application code
COPY . .

# Copy and set entrypoint
COPY entrypoint.sh /app/backend/entrypoint.sh
RUN chmod +x /app/backend/entrypoint.sh

# Create necessary directories
RUN mkdir -p uploads instance logs

# Set proper permissions
RUN chmod -R 755 uploads instance logs

# Clean up uv cache
RUN rm -rf /tmp/uv-cache

# Expose port
EXPOSE 5000

# Use entrypoint for auto-migration
ENTRYPOINT [ "./entrypoint.sh" ]
