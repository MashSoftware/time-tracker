FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1
COPY --chown=app run.sh /usr/local/bin/run-app
RUN chmod +x /usr/local/bin/run-app
COPY --chown=app requirements.txt .
RUN pip install -r requirements.txt
RUN useradd --create-home app
USER app
WORKDIR /home/app
COPY --chown=app . .
CMD ["run-app"]