# -*- coding: utf-8 -*-

""" Выборка самых популярных статей """

from flask import render_template, g


def view_pages_favorites(num=None):
    return render_template('favorites.html')
