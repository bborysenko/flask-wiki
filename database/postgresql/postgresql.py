# -*- coding: utf-8 -*-
""" Работа с Postgresql через SQLAlchemy """
#from flask import current_app
import os
import commands

import flask

from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from flask.ext.login import LoginManager,UserMixin,AnonymousUser,login_user,logout_user,current_user,login_required, make_secure_token

#import sphinxapi

import datetime

import models
from appwiki.methods.access import access_f

db  = SQLAlchemy()

def indexer():
    pass
#    os.system(ur"indexer --rotate --config /usr/local/etc/sphinx.conf --all")


def get_result_search(str_search, str_text, sub = False):
    begin_text = -1
    end_text = -1
    c_sim = 200
    begin_text = str_text.find( str_search )
    if begin_text != -1:
        if begin_text - c_sim > 0:
            begin_text = begin_text - c_sim
        else:
            begin_text = 0
        if begin_text + c_sim + len(str_search)< len(str_text):
            end_text = begin_text + c_sim + len(str_search)
        else:
            end_text = len(str_text)
    else:
        begin_text = 0
        end_text = c_sim

    text = str_text
    if sub is True:
        text = str_text[begin_text:end_text]
    if begin_text != -1:
        if sub is True:
            if begin_text != 0:
                text = "..." + text
            if end_text < len(str_text):
                text = text + "..."
        begin = (text.lower()).find(str_search.lower())
        if begin != -1:
            text = text[0:begin] + '<span style="background-color:yellow;size:15px;">' + text[begin:begin + len(str_search)] + "</span>" + text[begin + len(str_search):-1]
    return text


class Wiki(db.Model):
    __tablename__ = "wiki"
    __bind_key__ = 'wiki'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    access = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default = "NOW()")
    page = db.relationship("Page",
                            primaryjoin="and_(Page.wiki_id==Wiki.id, Page.active==True)",
                            uselist=False
                        )

    access_show = db.Column(db.String(250))


    def __init__(self, url, title, access, user, access_show):
        self.url = url
        self.title = title
        self.access = access
        self.user_id = user.id
        self.access_show = access_show


pages_tags = db.Table( 'pages_tags',
                        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                        db.Column('page_id', db.Integer, db.ForeignKey('pages.id')),
                        info={'bind_key': 'wiki'}
                     )

class Page(db.Model):
    __tablename__ = "pages"
    __bind_key__ = 'wiki'
    id = db.Column(db.Integer, primary_key = True)
    wiki_id = db.Column(db.Integer, db.ForeignKey('wiki.id'))
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    access_show = db.Column(db.String(250))
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
    __tablename__ = 'tags'
    __bind_key__ = 'wiki'
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
                        'access_show' : wiki.access_show,
                        'text' : wiki.page.text,
                        'title': wiki.title,
                        'url': wiki.url,
                        'tags' : [t.tag_name for t in wiki.page.tags],
                        'creation_date' : str(wiki.creation_date)[0:-7],
                        'modify_date' : str(wiki.page.creation_date)[0:-7]
                    }


    def insert_page( self, url, title, text, comment, user, tags, access, access_show ):
        user = models.User.query.filter_by(login=user).first()
        wiki = Wiki(url = url,
                    title = title,
                    access = access,
                    user  = user,
                    access_show = access_show
                   )
        page = Page(text = text,
                    user = user,
                    active = True,
                    comment = comment
                )
        tags = [t.replace(' ', '').strip() for t in tags.split(',')]
        for t in tags:
            tag = Tags.query.filter_by(tag_name=t).first()
            if tag is None:
                tag = Tags(t)
            page.tags.append(tag)

        page.wiki = wiki
        db.session.add(page)
        db.session.commit()

        # Индексация
        indexer()

    def update_page( self, url_page, url, title, text, comment, tags, user, access, access_show, active, update_title = False ):
        user = models.User.query.filter_by(login=user).first()
        wiki = Wiki.query.filter_by(url = url).first()
        act = True
        if active is False:
            act = False
        page = Page(text = text,
                    user = user,
                    active = act,
                    comment = comment
                )
        if active is True:
            wiki.page.active = False
        if update_title is True:
            wiki.title = title
#        wiki.x
        wiki.access = access
        wiki.access_show = access_show

        tags = [t.replace(' ', '').strip() for t in tags.split(',')]
        for t in tags:
            tag = Tags.query.filter_by(tag_name=t).first()
            if tag is None:
                tag = Tags(t)
            page.tags.append(tag)

        page.wiki = wiki

        db.session.add(page)
        db.session.commit()

        # Индексация
        indexer()

    # получает всю историю поста
    def get_pages_history( self, url ):
        wiki = Wiki.query.filter_by(url = url).first()
        if wiki is None:
            return None
        pages_list = []
        for d in wiki.pages:
            public = False
            if d.active == True :
                public = True
            user = models.User.query.filter_by(id=d.user_id).first()
            page = {
                'text' : d.text,
                'title' : wiki.title,
                'creation_date' : str(d.creation_date)[0:-7],
                'public' : public,
                'size' : len(d.text),
                'user' :  user.last_name + " " + user.first_name,
                'comment' : d.comment,
                '_id' : d.id
            }
            pages_list.append(page)

        return {'title': wiki.title, 'posts':pages_list, 'access_show': wiki.access_show, 'access': wiki.access}


    # получает пост с id == id_page из истории
    def get_page_history(self, url, page_id):
        wiki = Wiki.query.filter_by(url = url).first()
        if wiki is None:
            return None
        for d in wiki.pages:
            if int(page_id) == d.id:
                return { 'text' : d.text, 'title' : wiki.title }
        return None


    # Делает активной статью в истории
    def set_activity_history( self, url, page_id ):
        wiki = Wiki.query.filter_by(url = url).first()
        wiki.page.active = False
        db.session.query(Page).filter(Page.id == int(page_id)).update({'active': True})
        db.session.commit()

        # Индексация
        indexer()


    # поиск страниц по тегу
    def find_page_tags(self, tags):
        tags = [t.replace(';?!.:', '').strip() for t in tags.split(',')]

        arr_tags = Tags.query.filter(Tags.tag_name.in_(tags)).all()
        arr_id_tags = []

        if arr_tags is None:
            return None

        for d in arr_tags:
            arr_id_tags.append(d.id)

        pages = Page.query.filter_by(active=True).join(pages_tags).join(Tags).filter(Tags.id.in_(arr_id_tags))
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
                if d.title == "" or d.url == u'Служебная:Заглавная_страница':
                    continue
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
            if d.title == "" or d.url == u'Служебная:Заглавная_страница':
                continue
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
        result = db.session.execute(u"""SELECT UPPER(substring(title from 1 for 1)) AS alphabet,
                                    COUNT(substring(title from 1 for 1)) FROM wiki
                                    WHERE url != 'Служебная:Заглавная_страница'
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

    def get_result_search(self, str_search):
#        return None
#        client = sphinxapi.SphinxClient()
#        client.SetServer('127.0.0.1', 3312)
#        data = client.Query(str_search)
#        arr_id_pages = [d['id'] for d in data['matches'] ]
#
#        pages = Page.query.filter_by(active=True).filter(Page.id.in_(arr_id_pages))
#
#        pages = Page.query.filter_by(active=True).join(pages_tags).join(Tags).filter(Tags.id.in_(arr_id_tags))


#        wiki = Wiki.query.filter(Wiki.title.like(str_search)).filter(db.and_(Page.text.like(str_search), Page.active==True)).all()


        wiki = Wiki.query.filter(Wiki.title.ilike("%" + str_search + "%")).all()
        wiki_id = [w.id for w in wiki ]
        page = None
        page = Page.query.filter(
                                db.or_(
                                        db.and_( Page.text.ilike("%" + str_search + "%"), Page.active == True)
#                                                Page.wiki_id.in_(wiki_id)
                                        ,
                                        db.and_(
                                            Page.wiki_id.in_(wiki_id),
                                            Page.active == True
                                        )
                                    )
                            ).all()
#        page.y
        result = []
        for d in page:
            if d.wiki.url == u"Служебная:Заглавная_страница" or d.wiki.url == u"Служебная:Левое_меню":
                continue
            tags = [t.tag_name for t in d.tags]
            text = get_result_search( str_search, d.text, sub = True )
            title = get_result_search( str_search, d.wiki.title, sub = False )
            res = {
                    'title' : title,
                    'url' : d.wiki.url,
                    'text' : text,
                    'tags' : tags,
                    'creation_date' : str(d.wiki.creation_date)[0:10]
                }
            result.append(res)
        return result

    def get_all_users(self):
        users = models.User.query.order_by(models.User.last_name).all()
        result = []
        for d in users:
            res = {
                'first_name' : d.first_name,
                'last_name' : d.last_name,
                'login' : d.login,
                '_id' : d.id
            }
            result.append(res)
        return result

    def delete_page(self, word, page_id = None):
        if page_id is None:
            wiki = Wiki.query.filter_by(url = word).first()
            db.session.delete(wiki)
            db.session.commit()
            return 3

        page = Page.query.filter_by(id = page_id).first()
        if page is None:
            return 0
        if page.active == True:
            wiki = Wiki.query.filter_by(url = word).first()
            if wiki is None:
                return 0
            pages = Page.query.filter_by(wiki_id = wiki.id).all()
            if pages is None:
                return 0
            for page in pages:
                db.session.delete(page)
            db.session.delete(wiki)
            db.session.commit()
            return 2
        else:
            db.session.delete(page)
        db.session.commit()
        return 1

    def get_latedit_page(self):
        page = Page.query.filter(Page.active==True).order_by(Page.creation_date).all()
        result = []
        for d in page:
            if d.wiki is None:
                continue
            if d.wiki.title == "" or d.wiki.url == u"Служебная:Заглавная_страница" or d.wiki.url == u"Служебная:Левое_меню":
                continue
            tags = [t.tag_name for t in d.tags]

            user = models.User.query.filter_by(id=d.user_id).first()
            user_name = user.last_name + " " + user.first_name
            res = {
                'text' : d.text[0:300],
                'url' : d.wiki.url,
                'title' : d.wiki.title,
                'user' : user_name,
                'access' : d.wiki.access_show,
                'creation_date' : str(d.wiki.creation_date)[0:19],
                'modify_date' : str(d.creation_date)[0:19],
                'tags': tags
            }

            result.append(res)
        return result
