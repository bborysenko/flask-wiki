# -*- coding: utf-8 -*-
""" Работа с Postgresql через SQLAlchemy """
#from flask import current_app
import flask

from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from flask.ext.login import LoginManager,UserMixin,AnonymousUser,login_user,logout_user,current_user,login_required, make_secure_token

import datetime
from models import *

from appwiki.conf import *

db  = SQLAlchemy()

class Wiki(db.Model):
    __tablename__ = PREFIX + "wiki"
    __bind_key__ = 'psql'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    access = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default = "NOW()")
    page = db.relationship("Page",
                            primaryjoin="and_(Page.wiki_id==Wiki.id, Page.active==1)",
                            uselist=False
                        )



    def __init__(self, url, title, access, user):
        self.url = url
        self.title = title
        self.access = access
        self.user_id = user.id


pages_tags = db.Table( PREFIX + 'pages_tags',
                        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                        db.Column('page_id', db.Integer, db.ForeignKey('pages.id')),
                        info={'bind_key': 'psql'}
                     )

class Page(db.Model):
    __tablename__ = PREFIX + "pages"
    __bind_key__ = 'psql'
    id = db.Column(db.Integer, primary_key = True)
    wiki_id = db.Column(db.Integer, db.ForeignKey('wiki.id'))
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime, default = 'NOW()')

    wiki = db.relationship('Wiki',
                           backref=db.backref('pages', lazy='dynamic', order_by = creation_date),
                           uselist=False,
                           foreign_keys=wiki_id
                          )
    tags = db.relationship('Tags',
                            secondary=pages_tags,
                            backref=db.backref('pages', uselist=True, lazy="dynamic")
                          )

    def __init__(self, text, user, active, comment):
        self.text = text
        self.active = active
        self.comment = comment
        self.user_id = user.id


class Tags(db.Model):
    __tablename__ = PREFIX + 'tags'
    __bind_key__ = 'psql'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100))

    def __init__(self, tag_name):
        self.tag_name = tag_name


class Postgresql(object):

    def get_page(self, url = None):
        if url is None:
            return None
        else:
            wiki = Wiki.query.filter_by(url = url).first()
            if wiki is None:
                return None
            else:
                return {'access': wiki.access,
                        'text' : wiki.page.text,
                        'title': wiki.title,
                        'url': wiki.url,
                        'tags' : [t.tag_name for t in wiki.page.tags],
                        'creation_date' : str(wiki.creation_date)[0:-7],
                        'modify_date' : str(wiki.page.creation_date)[0:-7]
                    }


    def insert_page( self, url, title, text, comment, user, tags, access ):
        user = User.query.filter_by(login=user).first()
        wiki = Wiki(url = url,
                    title = title,
                    access = access,
                    user  = user
                   )
        page = Page(text = text,
                    user = user,
                    active = 1,
                    comment = comment
                )

        tags = [str(t.replace(';?!.:', '').strip()) for t in tags.split(',')]
        for t in tags:
            tag = Tags.query.filter_by(tag_name=t).first()
            if tag is None:
                tag = Tags(t)
            page.tags.append(tag)

        page.wiki = wiki
        db.session.add(page)
        db.session.commit()


    def update_page( self, url_page, url, title, text, comment, tags, user, access ):
        user = User.query.filter_by(login=user).first()
        wiki = Wiki.query.filter_by(url = str(url)).first()
        page = Page(text = text,
                    user = user,
                    active = 1,
                    comment = comment
                )
        wiki.page.active = 0
        wiki.access = access
        page.wiki = wiki

        tags = [str(t.replace(';?!.:', '').strip()) for t in tags.split(',')]
        for t in tags:
            tag = Tags.query.filter_by(tag_name=t).first()
            if tag is None:
                tag = Tags(t)
            page.tags.append(tag)

        db.session.add(page)
        db.session.commit()


    # получает всю историю поста
    def get_pages_history( self, url ):
        wiki = Wiki.query.filter_by(url = url).first()
        if wiki is None:
            return None
        pages_list = []
        for d in wiki.pages:
            public = False
            if d.active == 1:
                public = True
            page = {
                'text' : d.text,
                'title' : wiki.title,
                'creation_date' : str(d.creation_date)[0:-7],
                'public' : public,
                'size' : len(d.text),
                'user' :  User.query.filter_by(id=d.user_id).first().login,
                'comment' : d.comment,
                '_id' : d.id
            }
            pages_list.append(page)

        return {'title': wiki.title, 'posts':pages_list}


    # получает пост с id == id_page из истории
    def get_page_history(self, url, page_id):
        wiki = Wiki.query.filter_by(url = url).first()
        for d in wiki.pages:
            if int(page_id) == d.id:
                return { 'text' : d.text, 'title' : wiki.title }
        return None


    # Делает активной статью в истории
    def set_activity_history( self, url, page_id ):
        wiki = Wiki.query.filter_by(url = url).first()
        wiki.page.active = 0
        db.session.query(Page).filter(Page.id == int(page_id)).update({'active': 1})
#        db.session.query(Wiki).filter_by(url = url).update({'page.active':1}).first()
        db.session.commit()


    # поиск страниц по тегу
    def find_page_tags(self, tags):
        tags = [str(t.replace(';?!.:', '').strip()) for t in tags.split(',')]

        arr_tags = Tags.query.filter(Tags.tag_name.in_(tags)).all()
        arr_id_tags = []

        if arr_tags is None:
            return None

        for d in arr_tags:
            arr_id_tags.append(d.id)

        pages = Page.query.filter_by(active=1).join(pages_tags).join(Tags).filter(Tags.id.in_(arr_id_tags))
        result = []
        for page in pages:
            tags = [t.tag_name for t in page.tags]
            res = {
                    'title' : page.wiki.title,
                    'url' : page.wiki.url,
                    'text' : page.text,
                    'tags' : tags,
                    'creation_date' : str(page.creation_date)[0:10]
                }
            result.append(res)
        return result


    # алфавитный указатель
    def find_pages(self, letter):
        letter = letter.replace(""";?!.:@#$%^&*()-~_{}"' """, '')
        letter_lower = letter.lower()
        letter_upper = letter.upper()
        if len(letter_lower) != 1:
            return None
        wiki = Wiki.query.filter(db.or_(Wiki.title.startswith(letter_lower),Wiki.title.startswith(letter_upper) )).all()
        if wiki is None:
            return None
        else:
            result = []
            for d in wiki:
                tags = [t.tag_name for t in d.page.tags]
                res = {
                        'title' : d.title,
                        'url' : d.url,
                        'tags' : tags,
                        'creation_date' : str(d.page.creation_date)[0:10]
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
                'tags' : tags,
                'creation_date' : str(d.page.creation_date)[0:10]
            }
            result.append(res)
        return result

    def get_alphabet(self):
#        wiki = Wiki.query.filter_by(url = url).first()
#        result = db.session.query(db.func.substr(Wiki.title, 1, 1), db.func.substr(Wiki.title(1, 1)).count()).all()
#        result.x
#        result = Wiki.query(Wiki.title, db.func.substr(Wiki.title, 0, 1),label("total")).all()
        result = db.session.execute("""SELECT UPPER(substring(title from 1 for 1)) AS alphabet,
                                    COUNT(substring(title from 1 for 1)) FROM wiki
                                    GROUP BY alphabet ORDER BY alphabet
                                    """
                                   )
        alphabet_ru = {}
        alphabet_en = {}
        letters_en= u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letters_ru = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"
        for d in result:
            for letter in letters_en:
                if d[0] == letter:
                    alphabet_en[letter] = int(d[1])
                else:
                    if alphabet_en.get(letter) is None:
                        alphabet_en[letter] = 0
            for letter in letters_ru:
                if d[0] == letter:
                    alphabet_ru[letter] = int(d[1])
                else:
                    if alphabet_ru.get(letter) is None:
                        alphabet_ru[letter] = 0
        return {'en':alphabet_en, 'ru':alphabet_ru}
#        wiki = Wiki.query.filter(Wiki.title.startswith(letters)).group_by(Wiki.title).all()
