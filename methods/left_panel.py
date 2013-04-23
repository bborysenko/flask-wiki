# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import flask
import markdown2


def left_panel():
    page = flask.g.database.get_page("Служебная:Левое_меню")
    if page is not None:
#        text = markdown2.markdown(page['text'])
#        return text
        text = (page['text']).split('\r')
        result = ''
        for d in text:
          #  d.x
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
            if addres == u'Заглавная_страница':
                link = '<a href="' + flask.url_for('.view') + '">' + d[content_begin:content_end] + '</a>'
            elif addres == u'Все_статьи':
                link = '<a href="' + flask.url_for('.view_all_pages') + '">' + d[content_begin:content_end] + '</a>'
            elif addres == u'Алфавитный_указатель':
                link = '<a href="' + flask.url_for('.view_alphabet') + '">' + d[content_begin:content_end] + '</a>'
#            elif addres.find('http//') or addres.find('https//') or addres.find('https//'):
#                link = '<a href="' + addres + '">' + d[content_begin:content_end] + '</a>'
            elif addres[0:7] == 'http://' or addres[0:8] == 'https://' or addres[0:6] == "ftp://":
                link = '<a href="' + addres + '">' + d[content_begin:content_end] + '</a>'
            else:
                link = '<a href="' + flask.url_for('.view', word = addres) + '">' + d[content_begin:content_end] + '</a>'
            link = '<li>' + link + '</li>'
            result = result + link
        return result#.encode('utf-8')
    else:
        return ''

