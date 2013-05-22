# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from flask.ext.login import current_user
import flask

def delete_page(word, page_id = None):
    access = False
    if current_user.is_authenticated():
        if current_user.is_admin():
            access = True
    if access is False:
        return render_template('page.html',
                               page = None,
                               word = word,
                               message=u"Вы не имеете прав на удаление страниц"
                              )
    result = flask.g.database.delete_page(word, page_id)

    # ошибка
    if result == 0:
        return render_template('page.html',
                               page = None,
                               word = word,
                               message=u"Ошибка! Страница не найдена!"
                              )
    # удален устаревший пост
    elif result == 1:
        return redirect( url_for('.view_form_history', word=word) )
    # пост полностью удален
    elif result == 2 or result == 3:
        return redirect( url_for('.view', word = word) )


