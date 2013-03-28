# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
import flask

import textile
import markdown2

def get_url(word):
	url = word.strip()
	return url.replace(' ', '_')

def view(word = None):
    if word is None:
        return render_template('general.html')
    else:
        # Получаю страницу
        page = flask.g.database.get_page(get_url(word))
        if page is None:
            # Редирект на создание страницы
            return redirect(url_for('.get_form_edit', word = get_url(word)))
        else:
            # Вывод страницы
#            page['text'] = textile.textile(page['text'])
            page['text'] = markdown2.markdown(page['text'])
            return render_template('page.html', page = page, navigation = True, word = get_url(word) )
