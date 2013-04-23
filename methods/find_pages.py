# -*- coding: utf-8 -*-

from flask import render_template, request
import flask


def find_pages():
#    str_search = text_search
    str_search = request.form['search']
    pages = flask.g.database.get_result_search(str_search)

    return render_template('find.html', pages=pages, search_text=str_search)
