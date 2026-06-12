FROM python:3.10-slim

WORKDIR /app

# Install Chromium + driver for Selenium UI tests (run inside this container)
RUN apt-get update && apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        wget \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/lib/chromium:${PATH}"

COPY requirements.txt .

RUN pip install --no-cache-dir torch==2.3.0 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY tests/ tests/

RUN mkdir -p /app/logs

EXPOSE 5000

CMD ["python", "app.py"]
