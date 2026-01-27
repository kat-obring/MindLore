# Backend Dockerfile for development
FROM python:3.12-slim

WORKDIR /app

# Copy all source code first (needed for editable install)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Create var directory for SQLite database
RUN mkdir -p /app/var

EXPOSE 8000

CMD ["uvicorn", "app.main:create_app", "--factory", "--reload", "--host", "0.0.0.0", "--port", "8000"]
