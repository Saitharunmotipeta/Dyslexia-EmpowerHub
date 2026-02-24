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
# Working directory
# =========================
WORKDIR /app

# =========================
# Install system deps (minimal)
# =========================
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Python dependencies
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =========================
# Copy app
# =========================
COPY app ./app

# ❌ DO NOT copy .env into image (security)
# ❌ DO NOT copy softwaremodels

# =========================
# Expose port
# =========================
EXPOSE 8000

# =========================
# Run FastAPI
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]