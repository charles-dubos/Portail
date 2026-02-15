from .models import SQLCard, SQLPage, SQLSound
from flask_sqlalchemy import SQLAlchemy
from typing import Self

class PageIF:
    def __init__(self, db:SQLAlchemy, id:int=None) -> None:
        self.id = id
        self.db = db

    def create(self,
        title:str="",
        background_url:str="",
        ) -> Self:
        newPage = SQLPage(
            title=title,
            background_url=background_url,
            order=len(self.getList())+1
        )
        self.db.session.add( newPage )
        self.db.session.commit()
        self.id=newPage.id
        return self
    
    def delete(self) -> None:
        self.db.session.delete(self.get())
        self.db.session.commit()

    def update(self,
        title:str="",
        background_url:str="",
        order=None,
        ) -> Self:
        editPage = self.get()
        if title: editPage.title = title
        if background_url: editPage.background_url = background_url
        if order: editPage.order = order
        self.db.session.commit()
        return self

    def get(self) -> SQLPage:
        return self.db.session.execute(
                self.db.select(SQLPage).filter_by(id=self.id)
            ).one()[0]

    def getList(self) -> list[SQLPage]:
        return list(map( lambda i:i[0],
                self.db.session.execute(
                    self.db.select(SQLPage)
                        .order_by(SQLPage.order)
                ).all()
            ))



class CardIF:
    def __init__(self, db:SQLAlchemy, id:int=None, page_id:int=None) -> None:
        self.id = id
        self.db = db
        self.page_id = page_id

    def create(self,
        number:int,
        name:str="",
        logo_url:str="",
        link_url:str="",
        ) -> Self:
        newCard = SQLCard(
            page_id=self.page_id,
            number=number,
            name=name,
            logo_url=logo_url,
            link_url=link_url
        )
        self.db.session.add( newCard )
        self.db.session.commit()
        self.id=newCard.id
        return self
    
    def delete(self) -> None:
        self.db.session.delete(self.get())
        self.db.session.commit()

    def update(self,
        number:int,
        name:str="",
        logo_url:str="",
        link_url:str="",
        ) -> Self:
        editCard = self.get()
        if number: editCard.number=number
        if name: editCard.name=name
        if logo_url: editCard.logo_url=logo_url
        if link_url: editCard.link_url=link_url
        self.db.session.commit()
        return self

    def get(self) -> SQLCard:
        return self.db.session.execute(
                self.db.select(SQLCard).filter_by(id=self.id)
            ).one()[0]

    def getList(self) -> list[SQLCard]:
        return list(map( lambda i:i[0],
                    self.db.session.execute(
                        self.db.select(SQLCard)
                            .filter_by( page_id=self.page_id )
                            .order_by( SQLCard.number )
                        ).all()
                    ))

    def firstNumberAvailable(self) -> int:
        listOfCardsNumber = [ card.number for card in self.getList()]
        newNumber=1
        while newNumber in listOfCardsNumber: newNumber+=1
        return newNumber

    def isAvailable(self, number) -> bool:
        return False if number in [ card.number for card in self.getList()] \
            else True


class SoundIF:
    def __init__(self, db:SQLAlchemy, context:str=None) -> None:
        self.db = db
        self.context = context

    def update(self,
        url:str="",
        volume:int=None
        ) -> Self:
        editSound = self.get()
        if url: editSound.url=url
        if volume: editSound.volume=volume
        self.db.session.commit()
        return self

    def get(self) -> SQLSound:
        return self.db.session.execute(
                self.db.select(SQLSound).filter_by(context=self.context)
            ).one()[0]

    def getList(self) -> list[SQLSound]:
        return list(map( lambda i:i[0],
                    self.db.session.execute(
                        self.db.select(SQLSound)
                        ).all()
                    ))
