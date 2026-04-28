FROM    python:alpine
LABEL   maintainer="Papa Dub's" \
        version="26.04" \
        description="Conteneur portail WSGI Gunicorn"

ENV     APP_PATH="/portail"

WORKDIR $APP_PATH

ADD     . $APP_PATH

RUN     pip install --upgrade pip && pip install -e .

EXPOSE  8000

CMD     ["gunicorn", \
         "--config", "/portail/portail/gunicorn_config.py", \
         "portail:create_app()" ]

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
        CMD wget http://127.0.0.1:8000/health || exit 1
