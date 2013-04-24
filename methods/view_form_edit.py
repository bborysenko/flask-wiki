# -*- coding: utf-8 -*-
""" Возвращает форму для редактирования/создания записи """

from flask import render_template, request, redirect, url_for
import flask

from flask.ext.login import current_user

from appwiki.forms.create import CreateDataForm
from appwiki.forms.edit import EditDataForm, ServiceGeneralForm, ServiceLeftMenuForm

from appwiki.methods.access import access_f


def get_url(word):
    url = word.strip()
    return url.replace(' ', '_')


def get_word(url):
    return url.replace('_', ' ')


def view_form_edit(word):
    page = flask.g.database.get_page(get_url(word))
    access_edit = True
    if page is not None:
        # Проверка на права пользователя вносить правки в статью
        access_edit = access_f(page['access'], current_user)
        if current_user.is_authenticated():
            if current_user.is_admin():
                access_edit = True
#    return word

    if current_user.is_authenticated() is False or access_edit is False:
        return render_template('page.html',
                               page=None,
                               message=u"Вы не имеете прав на редaкатирование страницы",
                               navigation=True,
                               edit = True,
                               word=get_url(word)
                               )
    if current_user.is_admin() is False and (word == u"Служебная:Заглавная_страница" or word == u'Служебная:Левое_меню'):
        return render_template('page.html',
                               page=None,
                               message=u"Вы не имеете прав на редaкатирование страницы",
                               navigation=True,
                               edit = True,
                               word=get_url(word)
                            )
    if word == u"Служебная:Заглавная_страница":
        form = ServiceGeneralForm(request.form)
        action = u' создание '
        if page is not None:
            form.title.data = page['title']
            form.text.data = page['text']
            action = u" редактирование "
        return render_template('service_general_page.html',
                                form = form,
                                navigation=True,
                                edit = True,
                                word=get_url(word),
                                action_page = action
                              )

    if word == u"Служебная:Левое_меню":
        form = ServiceLeftMenuForm(request.form)
        action = u' создание '
        if page is not None:
            form.text.data = page['text']
            action = u" редактирование "
        return render_template('service_left_menu_page.html',
                                form = form,
                                navigation=True,
                                edit = True,
                                word=get_url(word),
                                action_page = action
                              )
    if page is None:
        # вывожу форму создания статьи
        form = CreateDataForm()
        form.title.data = get_word(word)
        form.access.data = current_user.login
        form.access_show.data = u'all'
        return render_template('form_create.html', form=form, word=get_url(word))
    else:
        # Вывожу форму редактирования статьи
        form = EditDataForm(request.form)
#        form.title.data = page['title']
        form.text.data = page['text']
        form.tags.data = ", ".join(page['tags'])
#        form.tags.data = page['tags']
        form.url.data = page['url']
        form.access.data = page['access']
        form.access_show.data = page['access_show']
        form.active.data = True
#        form.tags.data  = page['tags']
        return render_template('form_edit.html', form=form, navigation=True, edit = True, word=get_url(word))
