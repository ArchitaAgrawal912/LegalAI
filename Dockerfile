# 1. Use a specific, stable Python version
FROM python:3.11-slim

# 2. Prevent buffer/pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 3. Install system dependencies needed for libraries like asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 4. CRITICAL: Limit to 1 worker for low-memory instances
# Increase the timeout to 120s to allow model loading during startup
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", \
     "--workers", "1", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120"]