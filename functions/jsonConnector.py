import json, pathlib, logging, requests, uuid

DEFAULT_CONF='''
{
  "sounds": {
    "changePage": {
      "description": "Changement de page",
      "url": "https://universal-soundbank.com/sounds/1116.mp3", 
      "volume": "0.3"
    },
    "changeItem": {
      "description": "Changement d'entrée",
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


class Page:
  """Classe identifiant une page
  """
  title:str = ''
  dictOfCards:dict[Card] = {}
  img:str = ''

  def __init__(self,
               jsonPage:dict = None,
               ) -> None:
    if jsonPage:
      self.title = jsonPage['title']
      self.img = jsonPage['img']
      cards={}
      for number,card  in jsonPage['dictOfCards'].items():
        cards[number] = Card( card=card )
      self.dictOfCards = cards
    logging.debug(f"Création de la page '{self.title}'")

  def __len__(self) -> int:
    return len(self.dictOfCards)

  def getJson(self) -> dict:
    jsonPage = {
      'title':       self.title,
      'img':         self.img,
      'dictOfCards': {},
    }
    for number, card in self.dictOfCards.items():
      jsonPage['dictOfCards'][number] = card.getJson()
    return jsonPage
  
  def sortCards(self) -> None:
    self.dictOfCards = dict(sorted(self.dictOfCards.items(), key=lambda item: int(item[0])))


class Database:
  """Classe permettant la connexion à un fichier JSON 
  """
  path:str = None
  pages:dict[Page] = {}
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
      self.newPage( Page() )
      self.settings = json.loads(DEFAULT_CONF)
      self.save()

  def loadContent(self, content) -> any:
    # Reload settings
    self.settings = content['SETTINGS']

    # Reload pages
    self.pages = {}
    for name,jsonPage  in content['PAGES'].items():
      self.newPage(
        page=Page( jsonPage=jsonPage ),
        pageId=name
      )
    return self

  def save(self, sortPage=None) -> None:
    if sortPage:
      logging.debug(f"Tri des cartes de {sortPage}")
      self.pages[sortPage].sortCards()
    logging.info(f"Enregistrement de la base dans le fichier '{self.path}'")
    with open(file=self.path, mode='w', encoding='utf-8') as file:
      content = {
        "PAGES": {},
        "SETTINGS": self.settings,
      } 
      for pageId, page in self.pages.items():
        content['PAGES'][pageId] = page.getJson()
      json.dump(
        obj=content,
        fp=file,
        indent=2)

  def getPagesNames(self) -> list[str]:
    return list(self.pages.keys())

  def newPage(self, page:Page, pageId:str=None) -> str:
    if not pageId: pageId=str(uuid.uuid4())
    logging.warning(f"Création de la page {pageId}")
    self.pages[pageId] = page
    self.save()
    return pageId

  def delPage(self, pageId) -> Page:
    logging.warning(f"Suppression de la page {pageId}")
    page = self.pages[pageId]
    del self.pages[pageId]
    self.save()
    return page
