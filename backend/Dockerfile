FROM python:3.11-slim

WORKDIR /app

# Install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App
COPY app ./app
WORKDIR /app/app

ENV PYTHONUNBUFFERED=1

# ensure uploads and data dirs exist
RUN mkdir -p ./uploads ./data

# Start uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
