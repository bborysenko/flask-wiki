# -*- coding: utf-8 -*-
import flask
from flask import request, render_template
from appwiki.forms.create import FormCreate

def _get_url( word ):
    url = word.strip()
    return url.replace( ' ', '_' )

def view( word = None ):
    action = request.args.get('action')
    if word is None and action is None:
        return render_template( "general.html", navigetion = True )
    else:
            if action is None:
                return _get_page(word)
            else:
                if action == 'create':
                    return _get_form_create( word )
                elif action == 'edit':
                    return _get_form_edit(word)
                elif action == 'random':
                 # отдать рандомную статью
                     pass


# Создание формы показа статьи
def _get_form_create( word ):
    form = FormCreate()
    form.title.data = word
    return render_template('form.html', form = form)
def _get_form_edit(url):
    pass

def _get_page( word ):
    url = _get_url(word)
    page = flask.g.database.get_page(url)
    if page is None:
        return _get_form_create( word )
    else:
        return render_template( 'page.html', page = page, navigation = True )

