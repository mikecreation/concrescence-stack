# ---------------- Dockerfile ----------------
# Base image
FROM python:3.10-slim

# Create work directory inside the image
WORKDIR /app

# Copy everything from your repo into the image
COPY . /app

# Install Python packages if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Default command (harmless test message)
CMD ["python", "-c", "print('NEA Docker ready')"]
