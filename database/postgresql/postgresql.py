# -*- coding: utf-8 -*-
""" Работа с Postgresql через SQLAlchemy """

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker

engine = create_engine('postgresql://liveevents:liveevents@localhost/liveevents')
Base = declarative_base()
Base.metadata.create_all(engine)

class Wiki(Base):

    __tablename__ = "wiki"

    id = Column(Integer, primary_key = True, index = True)
    access = Column(String(250))
    creation_date = Column(Date,nullable = True)

#    page_id = None#db.Column(Integer, ForeignKey('pages.id'))
    page_id = Column(Integer, ForeignKey('pages.id'))
    #pages = db.relationship( 'Pages', backref=db.backref('pages', lazy='dynamic') )

    tags = None
#    title = Column(String(250))
#    text = Column(Text)
    url = Column(String(100))
    user_id = None #db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, access = None, tags = None, title = None, url = None, user = None):
        self.access = access
        self.title = title
        self.text = text
        self.url = url


class Pages(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key = True, index = True)
    comment = Column(String(250))
    wiki_id = None
    user_id = None
    tags = None
    title = Column(String(250))
    text = Column(Text)
    creation_date = Column(Date)

    def __init__(self, url = None, tags = None, user = None, title = None, text = None, creation_date = None):
        self.url = url
        self.user_id = user
        tags = none





class Postgresql(object):
    def get_page(self, url = None):
        return None
        if url is None:
            pass
        else:
            pass

    def insert_page( self, url, title, text, comment, user, tags, access ):
        engine.execute( 'INSERT INTO wiki( access, creation_date, tags, url, user_id ) VALUES ('+access+','+'2012-01-01,'+234+','+url+',1 )' )
