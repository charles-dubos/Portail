from functions.jsonConnector import *
from functions.cookieConf import *
import logging
from os.path import abspath, dirname, join
from os import pardir


# 'CONSTANTES paramétrables'
MAIN_DIR=abspath(join(dirname(__file__), '..'))
DATABASE_NAME=f'{MAIN_DIR}/monSite.json'
LOGFILE_PATH=f'{MAIN_DIR}/monSite.log'
LOGLEVEL=['NOTSET','DEBUG','INFO','WARNING','ERROR','CRITICAL'][1]

# Generating logging
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  filename=LOGFILE_PATH,
  level=getattr( logging, LOGLEVEL )
)


# FONCTIONS

## Chargement de la base
def loadDatabase() -> Database:
  logging.info("Chargement de la base {}".format(DATABASE_NAME))
  return Database(DATABASE_NAME)
  

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


# PRELOADING de la database et génération d'une conf vide
database = loadDatabase()
config = Configuration()
