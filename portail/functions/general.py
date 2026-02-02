from .jsonConnector import *
from flask import request
import logging


# load config variables
# DATABASE_NAME = ""
# LOGFILE_PATH = ""
# LOGLEVEL = ""

def loadLogging(logConfig: dict):
  logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=logConfig['LOGFILE_PATH'],
    level=getattr( logging, logConfig['LOGLEVEL'] )
  )


# FONCTIONS

## Chargement de la base
def loadDatabase(name:str) -> Database:
  logging.info("Chargement de la base {}".format(name))
  return Database(name)

## Récupération de cookie
def getCookie(database:Database,name:str) -> str:
  mainPage = request.cookies.get('mainPage')
  return mainPage if mainPage else database.getPagesId()[0]
  

## Navigation
def nextPage(database:Database,current:str)->str:
  listPages = database.getPagesId()
  return listPages[(listPages.index(current) +1) % len(listPages)]


def prevPage(database:Database,current:str)->str:
  listPages = database.getPagesId()
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
