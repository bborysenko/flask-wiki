# -*- coding: utf-8 -*-

from flask import render_template
import flask


def view_alphabet(letter=None):
    if letter is None or len(letter) != 1:
        alphabet = flask.g.database.get_alphabet()
#        alphabet.x
        return render_template('alphabet.html', alphabet = alphabet)
    else:
        pages = flask.g.database.find_pages(letter)
        try:
            if pages.count() == 0:
                pages = None
        except:
            pass
        return render_template('alphabet_find.html', pages=pages, search=letter)
