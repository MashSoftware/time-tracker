FROM python:3.13-slim

RUN addgroup --system app && adduser --system --group app

WORKDIR /home/app

# Set environment variables
ENV FLASK_APP=time_tracker.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY --chown=app:app app app
COPY --chown=app:app migrations migrations
COPY --chown=app:app time_tracker.py config.py docker-entrypoint.sh requirements.txt ./

RUN pip install -r requirements.txt \
    && chmod +x docker-entrypoint.sh

USER app

ENTRYPOINT ["./docker-entrypoint.sh"]
