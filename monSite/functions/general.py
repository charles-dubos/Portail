from monSite.functions.jsonConnector import *
import logging

# 'CONSTANTES paramétrables'
DATABASE_NAME='monSite.json'
DEFAULT_CONF={
    "modeSombre": "1",
    "logFile": "monSite.log",
    "logLevel": "DEBUG",
    "serverManagerUrl": "http://127.0.0.1:80"
}
# Generating logging
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.DEBUG
)


# FONCTIONS
## Chargement
def loadDatabase() -> Database:
  logging.info("Chargement de la base {}".format(DATABASE_NAME))
  # Chargement de la base
  database = Database(DATABASE_NAME)

  # pre-start checks
  logging.debug("Début des tests")
  startingChecks(database=database)

  return database


def startingChecks(database:Database) -> None:
  # Charge les confs, les initie le cas échéant, et vérifie une famille au moins
  logging.debug("Contrôle de la base.")

  # Vérifie la configuration par défaut
  for confKey in DEFAULT_CONF.keys():
    if confKey not in database.config.keys():
      logging.info(f"Clé de configuration '{confKey}' introuvable," +
                   f"initiée par défaut à '{DEFAULT_CONF[confKey]}'")
      database.config[confKey] = DEFAULT_CONF[confKey]

  # Rechargement du logging
  for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
  logging.basicConfig(
    filename=database.config['logFile'],
    level=getattr( logging, database.config['logLevel'] ),
  )
  logging.debug('Logging reconfiguré')

  # Création d'une famille par défaut si inexistante
  if not database.getFamiliesNames():
    logging.info("Pas de famille dans la base: création d'une famille par défaut")
    database.families['liens'] = Family(
      jsonFamily={
        "title":"Liens divers",
        "dictOfCards":{},
      }
    )

  # Vérifie la cohérence de la page principale
  if 'mainPage' not in database.config.keys() \
  or database.config['mainPage'] not in database.getFamiliesNames():
    logging.info("Clé de configuration 'mainPage' introuvable ou inconsistante," + 
      f"initiée par défaut à '{database.getFamiliesNames()[0]}'")
    database.config['mainPage'] = database.getFamiliesNames()[0]

  database.save()


## Navigation
def nextPage(database:Database,current:str)->str:
  listPages = database.getFamiliesNames()
  return listPages[(listPages.index(current) +1) % len(listPages)]


def prevPage(database:Database,current:str)->str:
  listPages = database.getFamiliesNames()
  return listPages[(listPages.index(current) -1) % len(listPages)]


def firstAvailable(database:Database,current:str)->str:
  for i in range(1, len(database.families[current])+2):
    if not str(i) in database.families[current].dictOfCards.keys():
      logging.debug(f"Premier nombre dispo: {str(i)}")
      return str(i)


## Card edition
def deleteCard(database: Database, familyId:str, cardId: str) -> None:
  logging.warning(f"Suppression de '{cardId}' dans la famille '{familyId}'")
  del database.families[familyId].dictOfCards[cardId]


def editCard(database:Database, 
             familyId:str,
              cardId:str,
              data:str) -> None:
  logging.info(f"Edition de la carte '{cardId}' dans la famille '{familyId}'")
  logging.debug(f"avec {data}")
  database.families[familyId].dictOfCards[cardId] = Card( data )


# PRELOADING
database = loadDatabase()
