#!/bin/bash
flask db upgrade
exec gunicorn --bind 0.0.0.0:5000 -w 4 --access-logfile - time_tracker:app