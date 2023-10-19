#!/bin/bash
flask db upgrade
openssl req -new -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=GB/ST=Devon/L=Plymouth/O=HM Land Registry/OU=DDaT/CN=localhost"
exec gunicorn --reload --certfile cert.pem --keyfile key.pem -b :8000 --access-logfile - --error-logfile - ddat-capability-assessment:app