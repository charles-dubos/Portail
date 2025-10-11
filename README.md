# site_pi.dubs

Site en Flask avec pages de liens et gestion de services actifs (cf. projet Server Manager, voir dépendances).

## Debug

Pour déboguer l'appli flask:

1/ Installation/activation du venv
2/ Exécution de l'appli flask
3/ Connexion via browser sur http://localhost:8000
```bash
source venv/bin/activate
python3 -m flask --app app run --port 8000 --debug
```



## Configuration et fonctionnement

### Configuration

La configuration est initiée au démarrage dans le fichier `monSite.json`. Par
 défaut au premier démarrage, il s'initie sur `localhost:80`.

### Utilisation

Une fois installé, ouvrir le browser sur la [page principale](http://localhost:80).

## Dépendances

Les dépendances suivantes sont identifiées (installées lors de l'exécution du
script d'installation):

- [PY3] Modules `flask` et `requests` (cf. requirements.txt)
- [PY3] Le [serverManager](https://github.com/charles-dubos/serverManager)
