flask db upgrade
exec gunicorn time_tracker:app \
    --bind :$FLASK_RUN_PORT \
    --threads $GUNICORN_THREADS \
    --timeout $GUNICORN_TIMEOUT