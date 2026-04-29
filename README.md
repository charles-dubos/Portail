# Portail de liens

Site en Flask avec pages de liens.

## Utilisation en WSGI (prod)

Créer l'environnement et installer l'app avec la commande:
```bash
python3 -m venv .venv 
&& source .venv/bin/activate
&& pip install -e .
```

Une fois installée, lancer l'application avec la commande
 `gunicorn --config portail/gunicorn_config.py 'portail:create_app()'`.


## Configuration et fonctionnement

### Configuration 

Il y a 3 niveaux de configuration:

Localisation | Contenu | Type | Nom
---|---|---|---
Serveur | Configuration générale | Variables d'enironnement (opt) | `PORTAIL_LOGLEVEL`, `PORTAIL_SECRETKEY`, `PORTAIL_SQLITE_FILE`
Serveur | Pages et cartes | Fichier | `monSite.db`
Client | Configurations locales (page princiale et sons) | Cookie | `config`

### Utilisation

Une fois installé, ouvrir le browser sur la [page principale](http://localhost:80).


## Dépendances

Les dépendances suivantes sont identifiées (installées lors de l'exécution du
script d'installation):

- [PY3] Modules `gunicorn`, `flask`, `Flask-Minify` et `requests` (cf. requirements.txt)


## Debug

Pour déboguer l'appli flask:

1/ Installation/activation du venv
2/ Exécution de l'appli flask
3/ Connexion via browser sur http://localhost:8000
```bash
source .venv/bin/activate
python3 -m flask --app portail run --port 8000 --debug
```


## Dépendances CDN

URL du CDN | Contexte | Template concerné
:---|:---|:---
https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css | PureCSS : layout de page | Tous
https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/grids-responsive-min.css | Grilles PureCSS | Tous
https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/js/all.min.js | Icônes FontAwesome | Tous
https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js | Liste à classer | Settings
