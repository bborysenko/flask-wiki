# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from flask.ext.login import current_user
import flask

def delete_page(word, page_id):
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
    flask.g.database.delete_page(word, page_id)

    return redirect( url_for('.view_form_history', word=word) )


