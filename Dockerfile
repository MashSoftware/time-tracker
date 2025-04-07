# Build stage
FROM python:3.13-slim AS builder

WORKDIR /build

# Install dependencies needed to build psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# Install requirements
COPY requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# Run stage
FROM python:3.13-slim

# Create app group and user
RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /home/appuser

# Set environment variables
ENV FLASK_APP=time_tracker.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependency needed to run psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev

# Copy and install requirements from build stage
COPY --chown=appuser:appgroup --from=builder /build/wheels /wheels
COPY --chown=appuser:appgroup --from=builder /build/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy runtime code
COPY --chown=appuser:appgroup app app
COPY --chown=appuser:appgroup migrations migrations
COPY --chown=appuser:appgroup --chmod=755 time_tracker.py config.py docker-entrypoint.sh  ./

USER appuser

ENTRYPOINT ["./docker-entrypoint.sh"]
