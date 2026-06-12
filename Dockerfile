FROM python:3.10-slim

# Working directory set karein
WORKDIR /app

# System dependencies install karein (Selenium headless ke liye)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    git \
    && rm -rf /var/lib/apt/lists/*

# Requirements copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baki saara application code copy karein
COPY . .

# Logs directory create karein
RUN mkdir -p /app/logs

# Port expose karein
EXPOSE 5000

# App chalane ki command
CMD ["python", "app.py"]
