import json, logging
from flask import request
from functions.jsonConnector import Database

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
      self.setCfg( key='mainPage', value=database.getFamiliesNames()[0])
      return False
