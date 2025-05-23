FROM jrottenberg/ffmpeg:4.4-ubuntu as ffmpeg

FROM python:3.10-slim

COPY --from=ffmpeg /usr/local /usr/local

RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
