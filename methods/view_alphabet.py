# -*- coding: utf-8 -*-

from flask import render_template
import flask

def view_alphabet(letter = None):
    if letter is None or len(letter) != 1:
        return render_template('alphabet.html')
    else:
        pages = flask.g.database.find_pages(letter)
        if pages.count() == 0:
            pages = None
        return render_template( 'alphabet_find.html', pages = pages, search = letter )
