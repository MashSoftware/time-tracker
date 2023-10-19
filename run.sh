#!/bin/bash

if [ -z "$DATABASE_URL" ]; then
    echo "\$DATABASE_URL is not set";
    exit 1
fi

if [ -z "$FLASK_RUN_PORT" ]; then
    echo "\$FLASK_RUN_PORT is not set";
    exit 1
fi

if [ -z "$GUNICORN_THREADS" ]; then
    echo "\$GUNICORN_THREADS is not set";
    exit 1
fi

if [ -z "$GUNICORN_TIMEOUT" ]; then
    echo "\$GUNICORN_TIMEOUT is not set";
    exit 1
fi

if [ -z "$MAILGUN_API_KEY" ]; then
    echo "\$MAILGUN_API_KEY is not set";
    exit 1
fi

if [ -z "$MAILGUN_API_URL" ]; then
    echo "\$MAILGUN_API_URL is not set";
    exit 1
fi

if [ -z "$REDIS_URL" ]; then
    echo "\$REDIS_URL is not set";
    exit 1
fi

if [ -z "$SECRET_KEY" ]; then
    echo "\$SECRET_KEY is not set";
    exit 1
fi

flask db upgrade
exec gunicorn time_tracker:app \
    --bind :$FLASK_RUN_PORT \
    --threads $GUNICORN_THREADS \
    --timeout $GUNICORN_TIMEOUT
