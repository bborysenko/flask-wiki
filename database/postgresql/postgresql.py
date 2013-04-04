# -*- coding: utf-8 -*-
""" Работа с Postgresql через SQLAlchemy """

from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin

import datetime

#from sqlalchemy import *
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relation, sessionmaker

#engine = create_engine('postgresql://liveevents:liveevents@localhost/liveevents')
#Base = declarative_base()

db = SQLAlchemy()

class Wiki(db.Model):
    __tablename__ = "wiki"
    id = db.Column(db.Integer, primary_key = True, index = True)
    url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    access = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime,nullable = True, default = datetime.datetime.now())
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)

    page = db.relation("Page", backref='wiki', lazy=True)

    all_pages = db.relationship("Page")
#    all_pages = db.relationship("Page", backref="awiki")

    def __init__(self, url, title, access, user_id):
        self.url = url
        self.title = title
        self.access = access
        self.user_id = user_id

class Page(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key = True, index = True)
#    wiki_id = Column(Integer, ForeignKey('wiki.id'), nullable=False)
    wiki_id = db.Column(db.Integer, default = 0)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    active = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime, default = datetime.datetime.now())

    #tags = db.relation("PageTag", uselist = True, backref = "page")
    tags = db.relationship("PageTag", backref="page")
    wiki_page = db.relationship("Wiki", backref="pages")

    def __init__(self, text, user_id, active, comment):
        self.text = text
        self.user_id = user_id
        self.active = active
        self.comment = comment

class PageTag(db.Model):
    __tablename__ = "pages_tags"
    id = db.Column(db.Integer, primary_key = True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
#        page = relation("PageTags", backref="tags", lazy = False)
#        page = Column(Integer, ForeignKey('pages.id'), default = 0)
    def __init__(self):
        pass


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key = True)
    tag = db.Column(db.String(100))
    tags = db.relation("PageTag", backref="pagestags", lazy = False)
    page_tags = db.relation("PageTag", backref='tag_name', lazy=False)
    def __init__(self, tag):
        self.tag = tag

#Base.metadata.create_all(engine)

class Postgresql(object):

    def get_page(self, url = None):
        try:
            wiki = Wiki.query.filter_by(url = str(url)).first()
            tags = []
            for d in wiki.page.tags:
                tags.append(d.tag_name.tag)
            return { 'access': wiki.access,
                    'text' : wiki.page.text,
                    'title': wiki.title,
                    'url': wiki.url,
                    'tags' : tags,
                    'creation_date' : ''
                   }
        except:
            return None



    def insert_page( self, url, title, text, comment, user, tags, access ):
        wiki = Wiki(url = url,
                    title = title,
                    access = access,
                    user_id = 1
                   )
        page = Page(text = text,
                    user_id = 1,
                    active = 1,
                    comment = comment
                )
        wiki.page = page
        db.session.add(wiki)
        db.session.commit()

        page.wiki_id = wiki.id
        arr_tags = [w.replace(';?!.:', '').strip() for w in tags.split(',')]
        for d in arr_tags:
            tag = Tag.query.filter_by(tag = str(d)).first()
            pt = PageTag()
            if tag is not None:
                pt.pagestags = tag
            else:
                pt.tag_name = Tag(str(d))
            page.tags.append( pt )
        db.session.commit()


    def update_page( self, url_page, url, title, text, comment, tags, user, access ):
        wiki = Wiki.query.filter_by(url = str(url)).first()
        page = Page(text = text,
                    user_id = 1,
                    active = 1,
                    comment = comment
                )
        page.wiki_id = wiki.id
        db.session.add(page)
        db.session.commit()

        wiki.page_id = page.id
        db.session.commit()

        page.wiki_id = wiki.id
        arr_tags = [w.replace(';?.!:', '').strip() for w in tags.split(',')]
        for d in arr_tags:
            tag = Tag.query.filter_by(tag = str(d)).first()
            pt = PageTag()
            if tag is not None:
                pt.pagestags = tag
            else:
                pt.tag_name = Tag(str(d))
            page.tags.append( pt )
        db.session.commit()

    # получает всю историю поста
    def get_pages_history( self, url ):
        wiki = Wiki.query.filter_by(url = str(url)).first()

        wiki
        wiki.z

        pages_list = []
        for d in pages:
            public = False
            if d.id == wiki.page_id:
                public = True

            page = {
                'text' : d.text,
                'title' : wiki.title,
                'creation_date' : d.creation_date,
                'public' : public,
                'size' : len(d.text),
                'user' : d.user_id,
                'comment' : d.comment,
                '_id' : d.id
            }
            pages_list.append(page)

        return {'title': wiki.title, 'posts':pages_list}


    # получает пост с id == id_page из истории
    def get_page_history(self, url, page_id):
        try:
            page = db.session.query(Page, Wiki).filter(Page.id == page_id).filter(Wiki.url == url).first()
            return { 'text' : page.Page.text, 'title' : page.Wiki.title }
        except:
            return None


    # Делает активной статью в истории
    def set_activity_history( self, url, page_id ):
        wiki = db.session.query(Wiki).filter_by(url=str(url)).first()
        db.session.query(Page).filter_by(wiki_id = wiki.id).update({'active':0})
        db.session.commit()
        db.session.query(Wiki).filter_by(url = url).update({'page_id':page_id})
        db.session.commit()
        db.session.query(Page).filter_by(id = page_id).update({'active':1})
        db.session.commit()


#    # Возвращает все страницы
#    def get_all_pages(self, page_num, page_size):
#        result = session.query(Pages).join(Wiki.id).filter_by(active=1)
#        return result
#

    # поиск страниц по тегу
    def find_page_tags(self, tags):
#        session = sessionmaker(engine)()
        arr_tags = [ w.strip(';?!: ') for w in tags.split(',')]

        tags = db.session.query(Tag).filter(Tag.tag.in_(arr_tags)).all()
        tags_id = []
        for d in tags:
            tags_id.append(d.id)

#        tags_pages =  PageTag.query.filter_by(tags_id.in_(tags_id)).distrinct().all()
        tags_pages = db.session.query(PageTag.page_id).filter(PageTag.tag_id.in_(tags_id)).distinct().all()
        pages_id = []
        for d in tags_pages:
            pages_id.append(d.page_id)

#        pages = db.session.query(Page).filter(Page.id.in_(pages_id)).all()
        data = db.session.query(Wiki, Page).filter(Page.id.in_(pages_id)).filter(Page.id == Wiki.page_id).filter(Page.active == 1).all()
        result = []
        for d in data:
#########################################################################################
            tags = db.session.query(PageTag).filter(PageTag.page_id == d.Page.id).all()
            tags_id = []
            for el in tags:
                tags_id.append(el.tag_id)
            tags_name = db.session.query(Tag).filter(Tag.id.in_(tags_id))
            tags_names = []
            for el in tags_name:
                tags_names.append(el.tag)
########################################################################################
                res = {
                    'title' : d.Wiki.title,
                    'url' : d.Wiki.url,
                    'text' : d.Page.text,
                    'tags' : tags_names
                }
                result.append(res)
        return result

    # алфавитный указатель
    def find_pages(self, letter):
        letter_lower = letter.lower()
        pages = db.session.query(Wiki, Page).filter(Wiki.title.like(letter_lower + "%"), Page.id == Wiki.page_id, Page.active == 1).all()

        result = []
        for d in pages:
################################################################################
            tags = db.session.query(PageTag).filter(PageTag.page_id == d.Page.id).all()
            tags_id = []
            for el in tags:
                tags_id.append(el.tag_id)

            tags_name = db.session.query(Tag).filter(Tag.id.in_(tags_id))
            tags_names = []
            for el in tags_name:
                tags_names.append(el.tag)
################################################################################
            res = {
                    'title' : d.Wiki.title,
                    'url' : d.Wiki.url,
                    'tags' : tags_names
            }
            result.append(res)
        return result

    def get_all_pages(self, page_num, page_size):
        # нужно для пагинации
        page_limit = page_size
        page_skip = 0
        if page_num is not None or int(page_num) != 0:
            page_skip = int(page_num) * int(page_size) - int(page_size)

#        wiki = Wiki.query.subquery()

        pages = db.session.query(Page).join(Wiki, Wiki.page_id == Page.id).all()
#        pages = db.session.query(Wiki, Page).filter(Page.active == 1).all()

        result = []
        for d in pages:
################################################################################
#            tags = db.session.query(PageTag).filter(PageTag.page_id == d.Page.id).all()
#            tags_id = []
#            for el in tags:
#                tags_id.append(el.tag_id)
#            tags_name = db.session.query(Tag).filter(Tag.id.in_(tags_id))
            tags_names = []
#            for el in tags_name:
#                tags_names.append(el.tag)
################################################################################
            res = {
                        'title' : d.text,
                        'url' : d.Wiki.url,
                        'tags' : tags_names
            }
            result.append(res)
        return result
