FROM python:3.11-slim

RUN useradd containeruser

WORKDIR /home/containeruser

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY app app
COPY time_tracker.py config.py docker-entrypoint.sh requirements.txt ./
RUN pip install -r requirements.txt \
    && chmod +x docker-entrypoint.sh \
    && chown -R containeruser:containeruser ./

# Set environment variables
ENV DATABASE_URL="postgresql://mash:mash@db:5432/time_tracker" \
    MAILGUN_API_KEY="" \
    MAILGUN_API_URL="" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    REDIS_URL="redis://cache:6379" \
    SECRET_KEY=27a832aa91849382e326b5200f2c3d748a78bac4587e6ffd626dd87d73438f44 \
    VERSION_NUMBER=Development

USER containeruser

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
