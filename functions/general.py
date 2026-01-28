from functions.jsonConnector import *
from functions.configure import Configuration
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
  listPages = database.getPagesNames()
  return listPages[(listPages.index(current) +1) % len(listPages)]


def prevPage(database:Database,current:str)->str:
  listPages = database.getPagesNames()
  return listPages[(listPages.index(current) -1) % len(listPages)]


def firstAvailable(database:Database,current:str)->str:
  for i in range(1, len(database.pages[current])+2):
    if not str(i) in database.pages[current].dictOfCards.keys():
      logging.debug(f"Premier nombre dispo: {str(i)}")
      return str(i)


## Card edition
def deleteCard(database: Database,
              pageId:str,
              cardId: str,
              save:bool=True) -> None:
  logging.warning(f"Suppression de '{cardId}' dans la page '{pageId}'")
  del database.pages[pageId].dictOfCards[cardId]
  if save: database.save()

def saveCard(database: Database,
            pageId:str,
            data: dict) -> None:
  if data['current'] != data['number']:
    deleteCard(
      database=database,
      pageId=pageId,
      cardId=data['current'],
      save=False
    )
    data['current'] = data['number']
  editCard(
    database=database,
    pageId=pageId,
    cardId=data['current'],
    data=data
  )


def editCard(database:Database, 
            pageId:str,
            cardId:str,
            data:dict) -> None:
  logging.info(f"Edition de la carte '{cardId}' dans la page '{pageId}'")
  logging.debug(f"avec {data}")
  database.pages[pageId].dictOfCards[cardId] = Card( data )
  database.save(sortPage=pageId)


## Page edition
def deletePage(database:Database,
              data:dict,
              pageName:str) -> str:
  path = nextPage(
    database=database,
    current=pageName
  )
  database.delPage( pageId=pageName )  
  return path

def createPage(database:Database,
              data:dict) -> str:
  path = database.newPage(
    page=Page( {
        'title': data['title'],
        'img': data['img'],
        'dictOfCards': {},
    } )
  )
  logging.info( f"Création de la page {path}" )
  logging.debug( f"avec les valeurs '{data['title']}', '{data['img']}'" )
  return path


# PRELOADING de la database et génération d'une conf vide
database = loadDatabase()
config = Configuration()
