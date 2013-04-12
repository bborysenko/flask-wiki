# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template
import flask

from flask.ext.login import current_user

from appwiki.methods.access import access_f

def get_url(word):
    url = word.strip()
    return url.replace(' ', '_')


def save_history(word):
    page_id = request.form['history']

    page = flask.g.database.get_page(get_url(word))
    if page is None:
        return None
    access_edit = True
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

    flask.g.database.set_activity_history(word, page_id)
    return redirect(url_for('.view', word=word))
