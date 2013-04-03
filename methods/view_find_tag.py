# -*- coding: utf-8 -*-
""" Поис по тегу. Страница зарезервированна. """
from flask import render_template
import flask


def view_find_tag(tags=None):
    if tags is None:
        pass
    else:
#        return "|" + tags + "|"
        pages = flask.g.database.find_page_tags(tags)
        return render_template('tags.html', pages=pages, tags=tags)
