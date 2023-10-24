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
ENV FLASK_APP=time_tracker.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER containeruser

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
