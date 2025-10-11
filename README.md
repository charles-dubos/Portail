# site_pi.dubs

Site en Flask avec pages de liens et gestion de services actifs.

## Installation & déploiement WSGI

Lancer le script `install.sh` avec l'utilisateur standard (depuis n'importe où,
 il faut juste que le fichier soit dans le répertoire définitif du
 site).

## Configuration et fonctionnement

### Configuration

La configuration est initiée au démarrage dans le fichier `monSite.json`. Par
 défaut au premier démarrage, il s'initie sur `localhost:80`.

> **NB:** En cas de modification des paramètres du serveur (répertoire, hôte,
> port), il convient de relancer le fichier `install.sh`.

### Utilisation

Une fois installé, ouvrir le browser sur la [page principale](http://localhost:80).

## Dépendances

Les dépendances suivantes sont identifiées (installées lors de l'exécution du
script d'installation):

- [PY3] Module `flask` et module `requests`
- [PY3] Le [serverManager](https://github.com/charles-dubos/serverManager)

## Debug

Rappel, pour déboger l'appli flask:

1/ Activation du venv
2/ Exécution de l'appli flask

```bash
source venv/bin/activate
python3 -m flask --app app run --port 8000 --debug
```
