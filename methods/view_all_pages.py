# -*- coding: utf- 8 -*-
from flask import render_template
import flask

from appwiki.methods.pagination import pagination

def view_all_pages(page_num = 1):

    page_size = 10
    # получаю страницы
    pages = flask.g.database.get_all_pages( page_num = page_num, page_size = page_size )
    # получаю размер всего
    count = flask.g.database.get_all_count()
    pag = pagination( count = count, size = page_size, numer = page_num, url = "/wiki/all/" )

    return render_template( 'all_pages.html', pages = pages, pagination = pag )
