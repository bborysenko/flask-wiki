# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
from flask.ext.login import current_user
import flask

import markdown2

from appwiki.methods.access import access_f
from appwiki.methods.left_panel import left_panel

def get_url(word):
    url = word.strip()
    return url.replace(' ', '_')



def view(word=None):
    if word is None:
        page = flask.g.database.get_page(get_url("Служебная:Заглавная_страница"))
        if page is None:
            if current_user.is_authenticated():
                if current_user.is_admin():
                    return redirect(url_for('.view_form_edit', word=get_url('Служебная:Заглавная_страница')))
            return render_template('general.html')
        else:
            page['text'] = markdown2.markdown(page['text'])
            if current_user.is_authenticated():
                if current_user.is_admin():
                    return render_template('general.html',
                                            page=page,
                                            navigation=True,
                                            read = True,
                                            word=get_url("Служебная:Заглавная_страница")
                                          )

            return render_template('general.html', page=page, navigation = False)
    else:
        # Получаю страницу
        page = flask.g.database.get_page(get_url(word))

        if word == u"Служебная:Заглавная_страница":
            if current_user.is_authenticated():
                if current_user.is_admin():
                    if page is None:
                        return redirect(url_for('.view_form_edit', word=get_url('Служебная:Заглавная_страница')))
                    else:
                        page['text'] = markdown2.markdown(page['text'])
                        return render_template('general.html', page=page, navigation=True, read = True, word=get_url(word))
            return render_template('general.html', page=page, word=get_url(word))


        if word == u"Служебная:Левое_меню":
            if current_user.is_authenticated():
                if current_user.is_admin():
                    if page is None:
                        return ''
                    else:
                        page['text'] = markdown2.markdown(page['text'])
                        return render_template('left_menu.html', page=page, navigation=True, read = True, word=get_url(word))
            return render_template('left_menu.html', page=page, word=get_url(word))

        if page is None:
            # Редирект на создание страницы
            return redirect(url_for('.view_form_edit', word=get_url(word)))
        else:
            # Вывод страницы
            access_show = True
#            if current_user.is_authenticated():
            access_show = access_f(page['access'], current_user)
            if access_show is False:
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
#            page.x
            return render_template('page.html', page=page, navigation=True, read = True, word=get_url(word))
