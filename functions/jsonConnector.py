import json, pathlib, logging, requests

DEFAULT_DB_CONTENT='''
{
  "FAMILIES": {
    "liens": {
      "title": "Liens divers",
      "img": "",
      "dictOfCards": {}
    }
  },
  "SETTINGS": {
    "sounds": {
      "changeFamily": {
        "description": "Changement de page",
        "url": "https://universal-soundbank.com/sounds/1116.mp3", 
        "volume": "0.3"
      },
      "changeItem": {
        "description": "Changement d'entrée'",
        "url": "https://universal-soundbank.com/sounds/7571.mp3", 
        "volume": "0.5"
      },
      "selectItem": {
        "description": "Validation d'entrée",
        "url": "https://universal-soundbank.com/sounds/9338.mp3", 
        "volume": "0.1"
      },
      "exitWindow": {
        "description": "Fermer l'application",
        "url": "https://universal-soundbank.com/sounds/9763.mp3", 
        "volume": "1"
      }
    }
  }
}
'''

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

  def __len__(self) -> int:
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
  
  def sortCards(self) -> None:
    self.dictOfCards = dict(sorted(self.dictOfCards.items(), key=lambda item: int(item[0])))


class Database:
  """Classe permettant la connexion à un fichier JSON 
  """
  path:str = None
  families:dict[Family] = {}
  settings:dict = {}

  def __init__(self,
               path:str,
               ) -> None:
    logging.debug(f"Initialisation de la base '{path}'")
    self.path = path
    self.load()

  def exists(self) -> bool:
    return pathlib.Path(self.path).exists()
      

  def load(self, strContent=None) -> None:
    logging.debug(f"Chargement du fichier")
    try:
      with open(file=self.path, mode='r', encoding='utf-8') as file:
        self.loadContent( content=json.load(fp=file) )
    except:
      self.loadContent( content=json.loads(s=DEFAULT_DB_CONTENT) ).save()

  def loadContent(self, content) -> any:
    # Reload settings
    self.settings = content['SETTINGS']

    # Reload families
    self.families = {}
    for name,jsonFamily  in content['FAMILIES'].items():
      self.newFamily(
        familyId=name, 
        family=Family( jsonFamily=jsonFamily )
      )
    return self

  def save(self, sortFamily=None) -> None:
    if sortFamily:
      logging.debug(f"Tri des cartes de {sortFamily}")
      self.families[sortFamily].sortCards()
    logging.info(f"Enregistrement de la base dans le fichier '{self.path}'")
    with open(file=self.path, mode='w', encoding='utf-8') as file:
      content = {
        "FAMILIES": {},
        "SETTINGS": self.settings,
      } 
      for familyId, family in self.families.items():
        content['FAMILIES'][familyId] = family.getJson()
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

