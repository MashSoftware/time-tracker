FROM python:3.13-slim

RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /home/appuser

# Set environment variables
ENV FLASK_APP=time_tracker.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY --chown=appuser:appgroup app app
COPY --chown=appuser:appgroup migrations migrations
COPY --chown=appuser:appgroup time_tracker.py config.py docker-entrypoint.sh requirements.txt ./

RUN pip install -r requirements.txt \
    && chmod +x docker-entrypoint.sh

USER appuser

ENTRYPOINT ["./docker-entrypoint.sh"]
