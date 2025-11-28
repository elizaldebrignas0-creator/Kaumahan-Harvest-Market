FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x start.sh

# Use build settings for Docker build (no external dependencies)
RUN python manage.py collectstatic --noinput --settings=kaumahan.settings_build

EXPOSE 8000

CMD ["./start.sh"]