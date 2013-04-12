# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
from flask.ext.login import current_user
import flask

import markdown2

from appwiki.methods.access import access_f

def get_url(word):
    url = word.strip()
    return url.replace(' ', '_')


def view(word=None):
    if word is None:
        return render_template('general.html')
    else:
        # Получаю страницу
        page = flask.g.database.get_page(get_url(word))
        if page is None:
            # Редирект на создание страницы
            return redirect(url_for('.view_form_edit', word=get_url(word)))
        else:
            # Вывод страницы
            access_show = True
#            if current_user.is_authenticated():
            access_show = access_f(page['access_show'], current_user)
            if current_user.is_authenticated():
                if current_user.is_admin():
                    access_show = True
            if access_show is False:
                 return render_template('page.html',
                                            page = None,
                                            message=u"Вы не имеете прав на просмотр страницы",
                                            navigation=True,
                                            word=word,
                                            read = True
                                        )
            page['text'] = markdown2.markdown(page['text'])
            return render_template('page.html', page=page, navigation=True, read = True, word=get_url(word))
