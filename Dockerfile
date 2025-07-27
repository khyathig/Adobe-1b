FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code from the src directory
COPY src/ /app/src/

# Set PYTHONPATH for module resolution
ENV PYTHONPATH=/app

# Run the main pipeline script
CMD ["python", "src/main.py", "input", "output"]