from .models import SQLCard, SQLPage, SQLSound
from flask_sqlalchemy import SQLAlchemy
from typing import Self

class PageIF:
    def __init__(self, db:SQLAlchemy, id:int=None) -> None:
        """Interface for SQLpage element.

        Args:
            db (SQLAlchemy): SQLA database.
            id (int, optional): Eventual page id. Defaults to None.
        """
        self.id = id
        self.db = db

    def create(self,
        title:str="",
        background_url:str="",
        ) -> Self:
        """Create a page in the database.

        Args:
            title (str, optional): Page title. Defaults to "".
            background_url (str, optional): Page background URL picture. Defaults to "".

        Returns:
            Self: Modified PageIF.
        """
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
        """Removes the page in SQLA database.
        Raise an error if only one page remains.

        Raises:
            Exception: If only one page.
        """
        if len(self.getList()) == 1 :
            raise Exception('Cannot delete the last page.')
        self.db.session.delete(self.get())
        self.db.session.commit()

    def update(self,
        title:str="",
        background_url:str="",
        order:int=None,
        ) -> Self:
        """Updates the selected page in SQLA database.

        Args:
            title (str, optional): Page title. Defaults to "".
            background_url (str, optional): Page background URL picture. Defaults to "".
            order (int, optional): Page order. Defaults to None.

        Returns:
            Self: Edited PageIF.
        """
        editPage = self.get()
        if title: editPage.title = title
        if background_url: editPage.background_url = background_url
        if order: editPage.order = order
        self.db.session.commit()
        return self

    def get(self) -> SQLPage:
        """Returns the SQLA element of selected page.

        Returns:
            SQLPage: The wanted page.
        """
        return self.db.session.execute(
                self.db.select(SQLPage).filter_by(id=self.id)
            ).one()[0]

    def getList(self) -> list[SQLPage]:
        """Returns the list of pages in the given SQLA database.

        Returns:
            list[SQLPage]: List of wanted pages.
        """
        return list(map( lambda i:i[0],
                self.db.session.execute(
                    self.db.select(SQLPage)
                        .order_by(SQLPage.order)
                ).all()
            ))



class CardIF:
    def __init__(self, db:SQLAlchemy, id:int=None, page_id:int=None) -> None:
        """Interface for SQLCard element.

        Args:
            db (SQLAlchemy): SQLA database.
            page_id (int, optional): Eventual page id. Defaults to None.
            id (int, optional): Eventual card id. Defaults to None.
        """
        self.id = id
        self.db = db
        self.page_id = page_id

    def create(self,
        number:int,
        name:str="",
        logo_url:str="",
        link_url:str="",
        ) -> Self:
        """Create a card in the database.

        Args:
            number (int): Card number.
            name (str, optional): Name of card. Defaults to "".
            logo_url (str, optional): URL for logo. Defaults to "".
            link_url (str, optional): URL of the link. Defaults to "".

        Raises:
            ValueError: If the number already exists for another card.

        Returns:
            Self: Modified CardIF.
        """
        if self.db.session.execute(
            self.db.select(SQLCard).filter_by(number=number,page_id=self.page_id)
            ).first() is not None:
            raise ValueError(f'Card {number} already exists.')
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
        """Removes the card in SQLA database.
        """
        self.db.session.delete(self.get())
        self.db.session.commit()

    def update(self,
        number:int,
        name:str="",
        logo_url:str="",
        link_url:str="",
        ) -> Self:
        """Updates the selected page in SQLA database.

        Args:
            number (int): Card number.
            name (str, optional): Name of card. Defaults to "".
            logo_url (str, optional): URL for logo. Defaults to "".
            link_url (str, optional): URL of the link. Defaults to "".

        Raises:
            ValueError: If the number already exists for another card.

        Returns:
            Self: Edited PageIF.
        """
        if (int(number) != self.get().number) \
          and (self.db.session.execute(
            self.db.select(SQLCard).filter_by(number=number,page_id=self.page_id)
            ).first() is not None) :
            raise ValueError(f'Card {number} already exists.')
        editCard = self.get()
        if number: editCard.number=number
        if name: editCard.name=name
        if logo_url: editCard.logo_url=logo_url
        if link_url: editCard.link_url=link_url
        self.db.session.commit()
        return self

    def get(self) -> SQLCard:
        """Returns the SQLA element of selected card.

        Returns:
            SQLCard: The wanted card.
        """
        return self.db.session.execute(
                self.db.select(SQLCard).filter_by(id=self.id)
            ).one()[0]

    def getList(self) -> list[SQLCard]:
        """Returns the list of cards in the given SQLA database.

        Returns:
            list[SQLCard]: List of wanted cards.
        """
        return list(map( lambda i:i[0],
                    self.db.session.execute(
                        self.db.select(SQLCard)
                            .filter_by( page_id=self.page_id )
                            .order_by( SQLCard.number )
                        ).all()
                    ))

    def firstNumberAvailable(self) -> int:
        """Returns the first number of card not attributed.

        Returns:
            int: Available number.
        """
        listOfCardsNumber = [ card.number for card in self.getList()]
        newNumber=1
        while newNumber in listOfCardsNumber: newNumber+=1
        return newNumber

    def isAvailable(self, number:int) -> bool:
        """Tests if card number is attributed or available.

        Args:
            number (int): Number to evaluate.

        Returns:
            bool: True or False...
        """
        return False if number in [ card.number for card in self.getList()] \
            else True


class SoundIF:
    def __init__(self, db:SQLAlchemy, context:str=None) -> None:
        """Creates a SQL sound setting.

        Args:
            db (SQLAlchemy): SQLA database.
            context (str, optional): Sound ID. Defaults to None.
        """
        self.db = db
        self.context = context

    def update(self,
        url:str="",
        volume:int=None
        ) -> Self:
        """Modifies the corresponding sound settings.

        Args:
            url (str, optional): URL of MP3 sound. Defaults to "".
            volume (int, optional): Volume percentage (0 to 100). Defaults to None.

        Returns:
            Self: SoundIF.
        """
        editSound = self.get()
        if url: editSound.url=url
        if volume: editSound.volume=volume
        self.db.session.commit()
        return self

    def get(self) -> SQLSound:
        """Returns the selected SQLSound.

        Returns:
            SQLSound: The SQLA sound element.
        """
        return self.db.session.execute(
                self.db.select(SQLSound).filter_by(context=self.context)
            ).one()[0]

    def getList(self) -> list[SQLSound]:
        """Returns the list of all SQLSound.

        Returns:
            list[SQLSound]: List of sounds in SQLA.
        """
        return list(map( lambda i:i[0],
                    self.db.session.execute(
                        self.db.select(SQLSound)
                        ).all()
                    ))
