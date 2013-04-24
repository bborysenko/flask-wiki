# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import flask
import markdown2
from flask.ext.login import current_user

def left_panel():
    result = ""
    page = flask.g.database.get_page("Служебная:Левое_меню")
    if page is not None:
        text = (page['text']).split('\r')
        for d in text:
            d = d.strip()
            content_end = d.find(']')
            content_begin = d.find('[')
            if content_end == -1 or content_begin == -1:
                continue

            link_begin = d.find('(')
            link_end = d.find(')')
            if link_begin < content_end or link_end < content_end:
                continue
            link_begin = link_begin + 1
            content_begin = content_begin + 1
            addres = d[link_begin:link_end]
            link = ""
            if addres == u'Заглавная_страница' or addres == u'Служебная:Заглавная_страница':
                link = '<a href="' + flask.url_for('.view') + '">' + d[content_begin:content_end] + '</a>'
            elif addres == u'Все_статьи':
                link = '<a href="' + flask.url_for('.view_all_pages') + '">' + d[content_begin:content_end] + '</a>'
            elif addres == u'Алфавитный_указатель':
                link = '<a href="' + flask.url_for('.view_alphabet') + '">' + d[content_begin:content_end] + '</a>'
            elif addres[0:7] == 'http://' or addres[0:8] == 'https://' or addres[0:6] == "ftp://":
                link = '<a href="' + addres + '">' + d[content_begin:content_end] + '</a>'
            else:
                link = '<a href="' + flask.url_for('.view', word = addres) + '">' + d[content_begin:content_end] + '</a>'
            link = '<li>' + link + '</li>'
            result = result + link

    lnk = ""
    if current_user.is_authenticated():
        if current_user.is_admin():
            lnk = u'<a href="' + flask.url_for('.view_form_edit', word = u'Служебная:Левое_меню') + u'">[Править]</a>'
            lnk =  '<div style="padding-top:5px;">' + lnk + '</div>'
    return result + lnk

