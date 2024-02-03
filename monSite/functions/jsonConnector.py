import json, pathlib, logging


class Server:
  """Services activables
  """
  name:str = None
  faIcon:str = None
  action:str = None
  state:str = 'stateERR'

  def __init__(self,
               jsonServer:dict,
               ) -> None:
    self.name = jsonServer['name']
    self.faIcon = jsonServer['faIcon']
    self.action = jsonServer['action']
    self.state = self.getState()

  def getJson(self) -> dict:
    return {
      'name':   self.name,
      'faIcon': self.faIcon,
      'action': self.action,
    }
  
  def getState(self) -> str:
    # Evaluation de l'état du serveur
    # self.state = 'stateON'
    # self.state = 'stateERR'
    # self.state = 'stateOFF'
    return self.state

  def switchState(self) -> None:
    # Switch de l'état
    states = ['stateERR', 'stateON', 'stateOFF']
    self.state = states[(states.index(self.state)+1)%3]
  
  
class Card:
  """Classe identifiant une carte
  """
  name:str = None
  picture:str = None
  comments:str = None
  url:str = None

  def __init__(self,
                card:dict,
                ) -> None:
    self.name =     card['name']
    self.picture =  card['picture']
    self.comments = card['comments']
    self.url =      card['url']

  def getJson(self) -> dict:
    return {
      'name':     self.name,
      'picture':  self.picture,
      'comments': self.comments,
      'url':      self.url,
    }


class Family:
  """Classe identifiant une famille
  """
  title:str = ''
  dictOfCards:dict[Card] = {}
  img:str=None

  def __init__(self,
               jsonFamily:dict,
               ) -> None:
    self.title = jsonFamily['title']
    self.img = jsonFamily['img']


    cards={}
    for number,card  in jsonFamily['dictOfCards'].items():
      cards[number] = Card( card=card )
    self.dictOfCards = cards

  def getJson(self) -> dict:
    jsonFamily = {
      'title':       self.title,
      'img':         self.img,
      'dictOfCards': {},
    }
    for number, card in self.dictOfCards.items():
      jsonFamily['dictOfCards'][number] = card.getJson()
    return jsonFamily

  def getCards(self) -> dict:
      return self.dictOfCards


class Database:
  """Classe permettant la connexion à un fichier JSON 
  """
  path:str = None
  config:dict = {}
  families:dict[Family] = {}
  servers:dict[Server] = {}

  def __init__(self,
               path:str,
               ) -> None:
    self.path = path
    logging.getLogger("monSite").debug('Chargement de la base.')
    if self.exists(): self.load()

  def exists(self) -> bool:
    return pathlib.Path(self.path).exists()
      
  def load(self) -> None:
    with open(file=self.path, mode='r', encoding='utf-8') as file:
      content = json.load(fp=file)
      
    # Reload families
    self.families = {}
    for name,jsonFamily  in content['FAMILIES'].items():
      logging.getLogger("monSite").debug(f'Chargement de la famille {name}.')
      self.families[name] = Family( jsonFamily=jsonFamily )

    # Reload Servers
    self.servers = {}
    for id, jsonServer in content['SERVERS'].items():
      self.servers[id] = Server( jsonServer=jsonServer )

    # Reload config
    self.config = content['CONFIGURATION']

  def save(self) -> None:
    with open(file=self.path, mode='w', encoding='utf-8') as file:
      content = {
        "FAMILIES":     {},
        "SERVERS":      {},
        "CONFIGURATION":self.config,
      }
      for familyId, family in self.families.items():
        content['FAMILIES'][familyId] = family.getJson()
      for serverId, server in self.servers.items():
        content['SERVERS'][serverId] = server.getJson()
      json.dump(
        obj=content,
        fp=file,
        indent=2)

  def getFamiliesNames(self) -> list[str]:
    return list(self.families.keys())

  def newFamily(self, familyId:str, family:Family) -> None:
    if not familyId or familyId in self.getFamiliesNames():
      raise Exception
    self.families[familyId] = family
    self.save()

  def delFamily(self, familyId) -> Family:
    family = self.families[familyId]
    del self.families[familyId]
    self.save()
    return family

  def newServer(self, serverId:str, server:Server) -> None:
    if not serverId or serverId in list(self.getServers().keys()):
      raise Exception
    self.servers[serverId] = server
    self.save()

  def delServer(self, serverId) -> Server:
    server = self.servers[serverId]
    del self.servers[serverId]
    self.save()
    return server

  def getServers(self) -> dict[Server]:
    return self.servers

  def getConfig(self) -> dict:
    return self.config
  
  def setConfig(self, key:str, value:object) -> None:
    self.config[key]=value
    self.save()
