FROM    alpine:latest
LABEL   maintainer="Papa Dub's" \
        version="25.09" \
        description="Conteneur portail WSGI Gunicorn"

ENV     APP_PATH="/portail"
ENV     VIRTUAL_ENV="/.venv"
ENV     PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR $APP_PATH

RUN     apk update \
 &&     apk add --no-cache python3 py3-pip \
 &&     python3 -m venv ${VIRTUAL_ENV} \
 &&     pip install --upgrade pip \
 &&     pip install -e . \
 &&     mkdir ./instance

ADD     . $APP_PATH

EXPOSE  8000

CMD     ["/.venv/bin/gunicorn", \
         "--config", "/portail/portail/gunicorn_config.py", \
         "portail:create_app()" ]

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
        CMD wget --spider http://127.0.0.1:8000/health
