# Dockerfile for IFC to Fragments Converter
FROM node:18-slim

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql-client \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create Python virtual environment
RUN python3 -m venv venv

# Copy requirements first for better caching
COPY requirements-minimal.txt .

# Install Python dependencies
RUN ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install -r requirements-minimal.txt

# Copy the frag_convert package
COPY frag_convert/ ./frag_convert/

# Install Node.js dependencies for the converter
WORKDIR /app/frag_convert
RUN npm install

# Go back to app directory
WORKDIR /app

# Copy the main script
COPY convert_ifc_to_fragments.py .

# Create directories for logs, reports, and data
RUN mkdir -p logs reports data/ifc data/fragments

# Create a non-root user (let system assign UID to avoid conflicts)
RUN useradd -m converter && \
    chown -R converter:converter /app

USER converter

# Set environment variables
ENV PYTHONPATH=/app
ENV PATH="/app/venv/bin:$PATH"

# Default command
CMD ["python", "convert_ifc_to_fragments.py"]
