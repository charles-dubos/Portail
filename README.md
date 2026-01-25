# site_pi.dubs

Site en Flask avec pages de liens.

## Utilisation en WSGI (prod)

Une fois les dépendances installées, lancer dans le répertoire de l'app la commande `gunicorn --config gunicorn_config.py app:app`.


## Configuration et fonctionnement

### Configuration  # A CORRIGER

Il y a 3 niveaux de configuration:

Localisation | Contenu | Type | Nom
---|---|---|---
Serveur | Pages et cartes | Fichier | `monSite.json` (défini dans `general.py`)
Client | Configurations locales (page princiale et sons) | Cookie | `config`
Client | Son muet ou non | Stockage JS persistant sur le serveur | `localStorage`

### Utilisation

Une fois installé, ouvrir le browser sur la [page principale](http://localhost:80).


## Dépendances

Les dépendances suivantes sont identifiées (installées lors de l'exécution du
script d'installation):

- [PY3] Modules `gunicorn`, `flask` et `requests` (cf. requirements.txt)


## Debug

Pour déboguer l'appli flask:

1/ Installation/activation du venv
2/ Exécution de l'appli flask
3/ Connexion via browser sur http://localhost:8000
```bash
source .venv/bin/activate
python3 -m flask --app app run --port 8000 --debug
```
