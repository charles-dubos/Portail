#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SITE_NAME="monSite"
APACHE_CONF_NAME="${SITE_NAME}.conf"
APACHE_SITE_DIR="/etc/apache2/sites-available/"
LOG_FILE="${SCRIPT_DIR}/${SITE_NAME}.log"

## Demande le MdP le cas échéant
sudo printf ""

printf "> Installation de Apache "
sudo apt update > ${LOG_FILE} 2>&1 && \
sudo apt -y install apache2 libapache2-mod-wsgi-py3 >> ${LOG_FILE} 2>&1 && \
sudo a2enmod wsgi ssl >> ${LOG_FILE} 2>&1


printf "[DONE]\n> Installation des dépendances python"
python3 -m pip install flask requests >> ${LOG_FILE} 2>&1


printf "[DONE]\n> Création de la configuration WSGI"
cd ${SCRIPT_DIR}
cat <<EOF > ${SITE_NAME}.wsgi
import sys, logging

sys.path.insert(0,"${SCRIPT_DIR}")

from ${SITE_NAME} import create_app
application = create_app()
EOF

printf "[DONE]\n> Lancement du site et reload Apache2"
python3 -c "from monSite.functions.general import generateApacheConf; generateApacheConf('${USER}', '${APACHE_CONF_NAME}')" >> ${LOG_FILE} 2>&1 &&\
sudo mv -f ${APACHE_CONF_NAME} ${APACHE_SITE_DIR} >> ${LOG_FILE} 2>&1 &&\
sudo a2ensite ${SITE_NAME} >> ${LOG_FILE} 2>&1; \
sudo systemctl reload apache2 >> ${LOG_FILE} 2>&1

printf "[DONE]\n"
