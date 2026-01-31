import json, logging
from flask import request
from .jsonConnector import Database

class Configuration:
  """Classe déterminant la configuration propre au device client
  """
  values:dict = {}

  def isSet(self):
    return bool(self.values)

  def getCfg(self,
          key:str):
    return self.values[key]

  def setCfg(self,
          key:str,
          value:str):
    self.values[key] = value

  def loads(self,
            strConfig:str) -> None:
    self.values = json.loads(strConfig)
  
  def dumps(self):
    return json.dumps(self.values)
  
  def loadFromCookies(self,
                      database:Database) -> bool:
    # Retourne vrai si cookie existant, faux sinon
    logging.info("Chargement à partir des cookies")
    cookieConf = request.cookies.get('config')

    # Génération si inexistante
    if ( cookieConf ):
      self.loads(cookieConf)
      return True
    else:
      logging.debug('Création de conf')
      self.setCfg( key='mainPage', value=database.getPagesNames()[0])
      return False


## Configuration edit

def saveConfig(database:Database,
              config:Configuration,
              data:dict
              ) -> bool:
  global setCookie
  setCookie = False
  logging.info( f"Enregistrement des configurations" )
  logging.debug( f"{config.getCfg('mainPage')}")
  if data['mainPage'] != config.getCfg('mainPage'):
    config.setCfg( key='mainPage', value=data['mainPage'] )
    logging.debug( f"Enregistrement de mainPage à la valeur {data['mainPage']}" )
    setCookie=True
  
  for sound in database.settings['sounds'].keys():
          database.settings['sounds'][sound]['url'] = data[f"{sound}-url"]
          database.settings['sounds'][sound]['volume'] = data[f"{sound}-volume"]
          logging.debug( f"Enregistrement de {sound} : url à {data[f"{sound}-url"]} et volume à {data[f"{sound}-volume"]}" )

  for page in database.pages.keys():
      database.pages[page].title = data[f"{page}-title"]
      database.pages[page].img = data[f"{page}-img"]

  database.save()
  return setCookie

setCookie=False
