from monSite.functions.jsonConnector import *

# 'CONSTANTES paramétrables'
DATABASE_NAME='monSite.json'

# FONCTIONS

## Chargement
def loadDatabase() -> Database:

  # Chargement de la base
  database = Database(DATABASE_NAME)

  # pre-start checks
  startingChecks(database=database)

  return database


def startingChecks(database:Database) -> None:
  # Crée la base de donnée le cas échéant ainsi qu'une famille au moins
  if not database.getFamiliesNames():
    database.families['liens'] = Family(
      jsonFamily={
        "title":"Liens divers",
        "dictOfCards":{},
      }
    )

  # Vérifie la configuration par défaut
  configuration = database.getConfig()
  if not configuration or \
    'mainPage' not in configuration.keys():
    database.setConfig(
      key='mainPage',
      value=database.getFamiliesNames()[0])
  else:
    if configuration['mainPage'] not in database.getFamiliesNames():
      database.setConfig(
        key='mainPage',
        value=database.getFamiliesNames()[0])


def getTitle(database:Database, current:str):
  return database.families[current].title


## Navigation
def nextPage(database:Database,current:str)->str:
  listPages = database.getFamiliesNames()
  return listPages[(listPages.index(current) +1) % len(listPages)]


def prevPage(database:Database,current:str)->str:
  listPages = database.getFamiliesNames()
  return listPages[(listPages.index(current) -1) % len(listPages)]


# PRELOADING
database = loadDatabase()
