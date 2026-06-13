FROM python:3.10-slim
WORKDIR /app
# Zaroori system tools ek hi layer mein install karein
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential git curl &&     rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
# Build process memory limit ke liye compile flag
RUN pip install --no-cache-dir --compile -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
