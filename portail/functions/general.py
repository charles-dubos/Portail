# from .jsonConnector import *
from flask import request
from flask_sqlalchemy import SQLAlchemy
from .models import SQLPage, SQLCard, SQLSound, db
from .interface import PageIF
import logging


def loadLogging(logConfig: dict):
  logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=logConfig['LOGFILE_PATH'],
    level=getattr( logging, logConfig['LOGLEVEL'] )
  )


# FONCTIONS

## Récupération de cookie
def getCookie(db:SQLAlchemy) -> int:
  mainPage = request.cookies.get('mainPage')
  return int(mainPage) if mainPage \
    else PageIF(db=db).getList()[0].id
  

## Navigation
# Replacing nextPage et prevPage
def movePage(db:SQLAlchemy,page_id:int, move:int) -> int:
  listOfPageId = [ page.id for page in PageIF(db=db).getList() ]
  return listOfPageId[(listOfPageId.index(int(page_id)) + move) % len(listOfPageId)]


def initDatabase(db:SQLAlchemy):
    initSound = []
    if not SQLSound.query.filter( SQLSound.context == "changePage" ).first():
        initSound.append( SQLSound(
                context = "changePage",
                description = "Changement de page",
                url = "https://universal-soundbank.com/sounds/1116.mp3",
                volume = 30
        ) )
    if not SQLSound.query.filter( SQLSound.context == "changeItem" ).first():
        initSound.append( SQLSound(
                context = "changeItem",
                description = "Changement d'entrée",
                url = "https://universal-soundbank.com/sounds/7571.mp3",
                volume = 50
        ) )
    if not SQLSound.query.filter( SQLSound.context == "selectItem" ).first():
        initSound.append( SQLSound(
                context = "selectItem",
                description = "Validation d'entrée",
                url = "https://universal-soundbank.com/sounds/9338.mp3",
                volume = 10
        ) )
    if not SQLSound.query.filter( SQLSound.context == "exitWindow" ).first():
        initSound.append( SQLSound(
                context = "exitWindow",
                description = "Fermer l'application",
                url = "https://universal-soundbank.com/sounds/9763.mp3",
                volume = 100
        ) )
    if initSound:
        db.session.add_all( initSound )
        db.session.commit()
    
    if not PageIF(db=db).getList():
        PageIF(db=db).create(
            title = "Default Page",
            background_url = "",
        )


## Card edition
# def deleteCard(database: Database,
#               pageId:str,
#               cardId: str,
#               save:bool=True) -> None:
#   logging.warning(f"Suppression de '{cardId}' dans la page '{pageId}'")
#   del database.pages[pageId].dictOfCards[cardId]
#   if save: database.save()

# def saveCard(database: Database,
#             pageId:str,
#             data: dict) -> None:
#   if data['current'] != data['number']:
#     deleteCard(
#       database=database,
#       pageId=pageId,
#       cardId=data['current'],
#       save=False
#     )
#     data['current'] = data['number']
#   editCard(
#     database=database,
#     pageId=pageId,
#     cardId=data['current'],
#     data=data
#   )


# def editCard(database:Database, 
#             pageId:str,
#             cardId:str,
#             data:dict) -> None:
#   logging.info(f"Edition de la carte '{cardId}' dans la page '{pageId}'")
#   logging.debug(f"avec {data}")
#   database.pages[pageId].dictOfCards[cardId] = Card( data )
#   database.save(sortPage=pageId)
