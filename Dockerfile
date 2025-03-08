FROM python:3.13-slim

RUN addgroup --system app && adduser --system --group app

WORKDIR /home/app

# Set environment variables
ENV FLASK_APP=time_tracker.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY app app
COPY migrations migrations
COPY time_tracker.py config.py docker-entrypoint.sh requirements.txt ./

RUN pip install -r requirements.txt \
    && chmod +x docker-entrypoint.sh \
    && chown -R app:app ./

USER app

ENTRYPOINT ["./docker-entrypoint.sh"]
