import json, pathlib, logging, requests


class Server:
  """Services activables
  """
  name:str = None
  faIcon:str = None
  daemon:str = None
  state:str = 'amber'

  def __init__(self,
               jsonServer:dict,
               ) -> None:
    logging.debug(f"Initialisation du serveur '{jsonServer['name']}'")
    self.name = jsonServer['name']
    self.faIcon = jsonServer['faIcon']
    self.daemon = jsonServer['daemon']

  def getJson(self) -> dict:
    return {
      'name':   self.name,
      'faIcon': self.faIcon,
      'daemon': self.daemon,
    }
  
  def getState(self, config) -> str:
    logging.info(f"Requête d'état du serveur '{self.name}'")

    try:
      response = requests.post(
        config["serverManagerUrl"]+"/status",
        data={ self.daemon:"" }
      ).json()
      self.state = ['green','red'][response[self.daemon]]
    except Exception:
      self.state = 'amber'

    logging.debug(f"Etat du serveur: '{self.state}'")
    return self.state

  def switchState(self, config) -> str:
    logging.warning(f"Requête de changement d'état du serveur '{self.name}'")
    logging.debug("Adresse: " + config["serverManagerUrl"]+"/switch")
    logging.debug( "Données: "+str({ self.daemon:"" }))

    try:
      response = requests.put(
        config["serverManagerUrl"]+"/switch",
        data={ self.daemon:"" }
      ).json()
      self.state = ['green','red'][response[self.daemon]]
    except Exception:
      self.state = 'amber'

    logging.debug(f"Nouvel état du serveur: '{self.state}'")
    return self.state
  
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
    logging.debug(f"Création de la carte #{card['name']}")
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
    logging.debug(f"Création de la famille '{jsonFamily['title']}'")
    self.title = jsonFamily['title']
    self.img = jsonFamily['img']

    cards={}
    for number,card  in jsonFamily['dictOfCards'].items():
      cards[number] = Card( card=card )
    self.dictOfCards = cards

  def __len__(self):
    return len(self.dictOfCards)

  def getJson(self) -> dict:
    jsonFamily = {
      'title':       self.title,
      'img':         self.img,
      'dictOfCards': {},
    }
    for number, card in self.dictOfCards.items():
      jsonFamily['dictOfCards'][number] = card.getJson()
    return jsonFamily


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
    logging.debug(f"Initialisation de la base '{path}'")
    self.path = path
    if self.exists(): self.load()

  def exists(self) -> bool:
    return pathlib.Path(self.path).exists()
      

  def load(self) -> None:
    logging.debug(f"Chargement du fichier")
    with open(file=self.path, mode='r', encoding='utf-8') as file:
      content = json.load(fp=file)
      
    # Reload config
    self.config = content['CONFIGURATION']

    # Reload families
    self.families = {}
    for name,jsonFamily  in content['FAMILIES'].items():
      self.newFamily(
        familyId=name, 
        family=Family( jsonFamily=jsonFamily )
      )

    # Reload Servers
    self.servers = {}
    for id, jsonServer in content['SERVERS'].items():
      self.newServer(
        serverId=id,
        server=Server( jsonServer=jsonServer )
      )
      self.getServerState(id)


  def save(self) -> None:
    logging.info(f"Enregistrement de la base dans le fichier '{self.path}'")
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
      logging.error(f"Impossible de créer la famille {familyId}")
      return None
    logging.warning(f"Création de la famille {familyId}")
    self.families[familyId] = family
    self.save()

  def delFamily(self, familyId) -> Family:
    logging.warning(f"Suppression de la famille {familyId}")
    family = self.families[familyId]
    del self.families[familyId]
    self.save()
    return family

  def newServer(self, serverId:str, server:Server) -> None:
    if not serverId or serverId in list(self.servers.keys()):
      logging.error(f"Impossible de créer le serveur {serverId}")
      return None
    logging.warning(f"Création du serveur {serverId}")
    self.servers[serverId] = server
    self.save()

  def delServer(self, serverId) -> Server:
    logging.warning(f"Suppression du serveur {serverId}")
    server = self.servers[serverId]
    del self.servers[serverId]
    self.save()
    return server
  
  def getServerState(self, serverId) -> str:
    return self\
      .servers[serverId]\
        .getState(self.config)

  def switchServerState(self, serverId) -> str:
    return self\
      .servers[serverId]\
        .switchState(self.config)
