FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and config
COPY src/ /app/src/
COPY config.py /app/

# Copy data directory (ensure input files are in data/input/)
COPY data/ /app/data/

# Set PYTHONPATH for module resolution
ENV PYTHONPATH=/app

# Run the main pipeline script
CMD ["python", "src/main.py", "data/input", "data/output"]
