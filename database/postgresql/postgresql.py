# -*- coding: utf-8 -*-
""" Работа с Postgresql через SQLAlchemy """

from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin

import datetime
#from models import db

db  = SQLAlchemy()


pages_tags = db.Table('pages_tags',
                          db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                          db.Column('page_id', db.Integer, db.ForeignKey('pages.id'))
                     )


class Wiki(db.Model):
    __tablename__ = "wiki"
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    access = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default = "NOW()")

    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))

    page = db.relationship("Page", uselist=False, foreign_keys = page_id)

    def __init__(self, url, title, access, user_id):
        self.url = url
        self.title = title
        self.access = access
        self.user_id = user_id


class Page(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key = True)
    wiki_id = db.Column(db.Integer, db.ForeignKey('wiki.id'))
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
#    creation_date = db.Column(db.DateTime, default = datetime.datetime.now())
    creation_date = db.Column(db.DateTime, default = "NOW()")

    wiki = db.relationship("Wiki", backref="pages", uselist=True, lazy='dynamic', foreign_keys=wiki_id)
    tags = db.relationship('Tags',
                            secondary=pages_tags,
                            backref=db.backref('pages', lazy='dynamic')
                          )


    def __init__(self, text, user_id, active, comment):
        self.text = text
        self.user_id = user_id
        self.active = active
        self.comment = comment


class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100))

    def __init__(self, tag_name):
        self.tag_name = tag_name


class Postgresql(object):

    def get_page(self, url = None):
        if url is None:
            return None
        else:
            wiki = Wiki.query.filter_by(url = str(url)).first()
            if wiki is None:
                return None
            else:
                tags = [t.tag_name for t in wiki.page.tags]
                return { 'access': wiki.access,
                        'text' : wiki.page.text,
                        'title': wiki.title,
                        'url': wiki.url,
                        'tags' : tags,
                        'creation_date' : wiki.creation_date,
                        'modify_date' : wiki.page.creation_date
                        }


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

        tags = [str(t.replace(';?!.:', '').strip()) for t in tags.split(',')]
        for t in tags:
            tag = Tags.query.filter_by(tag_name=t).first()
            if tag is None:
                tag = Tags(t)
            page.tags.append(tag)

        wiki.page = page
#############################################################
        db.session.add(wiki)
        db.session.commit()
        wiki.page.wiki_id = wiki.id
############################################################
#        page.wiki = [wiki]

        db.session.add(wiki)
        db.session.commit()


    def update_page( self, url_page, url, title, text, comment, tags, user, access ):
        wiki = Wiki.query.filter_by(url = str(url)).first()
        page = Page(text = text,
                    user_id = 1,
                    active = 1,
                    comment = comment
                )
        # изменения атрибут active в 0
        wiki.page.active = 0
        db.session.add(wiki)
        db.session.commit()

        tags = [str(t.replace(';?!.:', '').strip()) for t in tags.split(',')]
        for t in tags:
            tag = Tags.query.filter_by(tag_name=t).first()
            if tag is None:
                tag = Tags(t)
            page.tags.append(tag)
############################################
        page.wiki_id = wiki.id
        wiki.page = page
#########################################
        db.session.add(wiki)
        db.session.commit()


    # получает всю историю поста
    def get_pages_history( self, url ):
        wiki = Wiki.query.filter_by(url = str(url)).first()
        pages_list = []
        for d in wiki.pages:
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
        wiki = Wiki.query.filter_by(url = str(url)).first()
        for d in wiki.pages:
            if int(page_id) == d.id:
                return { 'text' : d.text, 'title' : wiki.title }
        return None


    # Делает активной статью в истории
    def set_activity_history( self, url, page_id ):
        wiki = Wiki.query.filter_by(url = str(url)).first()
        for d in wiki.pages:
            if int(page_id) == d.id:
                wiki.page = d
        db.session.add(wiki)
        db.session.commit()


    # поиск страниц по тегу
    def find_page_tags(self, tags):
        tags = [str(t.replace(';?!.:', '').strip()) for t in tags.split(',')]
        data_tags = Tags.query.filter(Tags.tag_name.in_(tags)).first()

        result = []
        for d in data_tags.pages:
            if int(d.active) != 1:
                continue
            tags = [t.tag_name for t in d.tags]
            res = {
                    'title' : d.wiki[0].title,
                    'url' : d.wiki[0].url,
                    'text' : d.text,
                    'tags' : tags
                }
            result.append(res)
        return result


    # алфавитный указатель
    def find_pages(self, letter):
        letter_lower = letter.lower()
        if len(letter_lower) != 1:
            return None

        wiki = Wiki.query.filter(Wiki.title.like(letter_lower + "%")).all()

        if wiki is None:
            return None
        else:
            result = []
            for d in wiki:
                tags = [t.tag_name for t in d.page.tags]
                res = {
                        'title' : d.title,
                        'url' : d.url,
                        'tags' : tags
                    }
                result.append(res)
            return result


    def get_all_pages(self, page_num, page_size):
        # нужно для пагинации
        page_limit = page_size
        page_skip = 0
        if page_num is not None or int(page_num) != 0:
            page_skip = int(page_num) * int(page_size) - int(page_size)

        wiki = Wiki.query.all()
        result = []
        for d in wiki:
            tags = [t.tag_name for t in d.page.tags]
            res = {
                'title' : d.title,
                'url' : d.url,
                'text' : d.page.text,
                'tags' : tags
            }
            result.append(res)
        return result
