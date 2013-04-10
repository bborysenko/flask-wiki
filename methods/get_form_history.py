# -*- coding: utf-8 -*-
""" Показывает все правки которые производились со статьей """

from flask import render_template, redirect, url_for
import flask

from flask.ext.login import current_user

from appwiki.methods.access import access_f


def get_url(word):
    url = word.strip()
    return url.replace(' ', '_')


def get_form_history(word=None):
    page = flask.g.database.get_page(get_url(word))
    access_edit = True
    if page is not None:
        # Проверка на права пользователя вносить правки в статью
        access_edit = access_f(page['access'], current_user)
    if current_user.is_admin():
         access_edit = True

    if current_user.is_authenticated() is False or access_edit is False:
        return render_template('page.html',
                               page=page,
                               message=u"Вы не имеете прав на просмотр истории изменения страницы",
                               navigation=True,
                               word=get_url(word),
                               history = True
                               )

    pages = flask.g.database.get_pages_history(get_url(word))
#    if pages is None:
#        return 'error!'
#    else:
    return render_template('history.html', pages=pages, word=get_url(word), navigation=True, history = True)
