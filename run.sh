flask db upgrade && gunicorn -b 0.0.0.0:$FLASK_RUN_PORT time_tracker:app
