from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SQLPage(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    title = db.Column(db.String(50), unique=True)
    background_url = db.Column(db.String(120))
    # cards = db.relationship("SQLCard", back_populates="pages")

class SQLCard(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), unique=True)
    logo_url = db.Column(db.String(120))
    link_url = db.Column(db.String(120))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    # page = db.relationship("SQLPage", back_populates="cards")
    db.UniqueConstraint('page_id', 'number', name='Single_couple')


class SQLSound(db.Model):
    __tablename__ = 'soundSettings'
    context = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(80))
    url = db.Column(db.String(120))
    volume = db.Column(db.Integer, nullable=False)
