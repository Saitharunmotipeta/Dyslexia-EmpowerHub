# =========================
# Base image
# =========================
FROM python:3.11-slim

# =========================
# Environment settings
# =========================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# =========================
# System dependencies
# =========================
# ffmpeg  → audio processing
# espeak  → TTS backend
# build-essential → some python wheels need it
# libsndfile1 → audio I/O safety
# =========================
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak \
    libsndfile1 \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Working directory
# =========================
WORKDIR /app

# =========================
# Python dependencies
# =========================
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =========================
# Copy application code
# =========================
COPY app ./app
COPY softwaremodels ./softwaremodels
COPY .env .env

# =========================
# Expose port
# =========================
EXPOSE 8000

# =========================
# Run FastAPI
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
