# 1. Use the official, lightweight Python image
FROM python:3.11-slim

# 2. Stop Python from creating .pyc files and force logs to print immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the directory inside the container
WORKDIR /app

# 4. Copy requirements first to leverage Docker caching
COPY requirements.txt .

# 5. Install dependencies securely
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application code
COPY . .

# 7. Expose the port Uvicorn will run on
EXPOSE 8000

# 8. Start the FastAPI application using Gunicorn for production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--workers", "4", "--bind", "0.0.0.0:8000"]