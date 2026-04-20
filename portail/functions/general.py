from flask import request
from flask_sqlalchemy import SQLAlchemy
from .models import SQLPage, SQLCard, SQLSound, db
from .interface import PageIF
import sys, logging, json


def loadLogging(logConfig: dict) -> None:
  """Configures logging.
  """
  logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    level=getattr( logging, logConfig['LOGLEVEL'] )
  )


# FONCTIONS
def getCookie(db:SQLAlchemy) -> int:
  """Request cookie if exists, return the first page if not set.

  Args:
      db (SQLAlchemy): SQLA database.

  Returns:
      int: id of main page.
  """
  mainPage = request.cookies.get('mainPage')
  return int(mainPage) if mainPage \
    else PageIF(db=db).getList()[0].id
  

## Navigation
def movePage(db:SQLAlchemy,page_id:int, move:int) -> int:
  """Get the previous or next page after collecting masked pages cookies.

  Args:
      db (SQLAlchemy): SQLA databse.
      page_id (int): current page.
      move (int): number of page (signed) wanted from the current page.

  Returns:
      int: Id of the page after move.
  """
  maskPages = request.cookies.get('maskPages')
  maskPages = [ int(id) for id in json.loads(maskPages)] if maskPages else []

  listOfPageId = [ page.id
                    for page in PageIF(db=db).getList()
                      if page.id not in maskPages ]

  return listOfPageId[
            (listOfPageId.index(int(page_id)) + move) % len(listOfPageId)
          ]

def initDatabase(db:SQLAlchemy) -> None:
  """Initiates the given database if empty.

  Args:
      db (SQLAlchemy): SQLA database.
  """
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
