# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for
import flask

from flask.ext.login import current_user

from appwiki.forms.create import CreateDataForm
from appwiki.forms.edit import EditDataForm

from appwiki.methods.access import access_f


def get_url(word):
#    url = word.encode('utf-8')
    url = word.strip()
    return url.replace(' ', '_')


def save_edit(word=None):
    # Получаю статьью из БД
    page = flask.g.database.get_page(get_url(word))
    url = get_url(word)
    access_edit = True
    if page is not None:
        # Проверка на права пользователя вносить правки в статью
        access_edit = access_f(page['access'], current_user)
    if current_user.is_authenticated() is False or access_edit is False:
        return render_template('page.html',
                               page=page,
                               message=u"Вы не имеете прав на редaкатирование страницы",
                               navigation=True,
                               word=word,
                               edit = True
                               )

    if page is None:
        form = CreateDataForm(request.form)
         # Создаю новую статью
        if form.validate():
            # Получаю данные из формы
            url = get_url(form.title.data)
            title = form.title.data.strip()
            text = form.text.data.strip()
            tags = form.tags.data.strip()
            comment = form.comment.data.strip()
            access = form.access.data.strip()
            # Сохраняю данные в БД
            flask.g.database.insert_page(url=url,
                                         title=title,
                                         text=text,
                                         user=current_user.login,
                                         comment=comment,
                                         tags=tags,
                                         access=access
                                         )
            # Редирект на созданную страницу
            return redirect(url_for('.view', word=get_url(title)))
        else:
            return render_template('form_create.html', form=form)
    else:
        form = EditDataForm(request.form)
        if form.validate():
            # Получение данных из формы
#            url = get_url(form.title.data)
#            title = form.title.data.strip()
            text = form.text.data.strip()
            tags = form.tags.data.strip()
            comment = form.comment.data.strip()
            access = form.access.data.strip()
            # URL имеющейся страницы
            url_page = form.url.data.strip()
            flask.g.database.update_page(url=url,
                                         url_page=url_page,
                                         title=None,
                                         text=text,
                                         user=current_user.login,
                                         comment=comment,
                                         tags=tags,
                                         access=access
                                         )
            return redirect(url_for('.view', word=url))
        else:
            return render_template('form_edit.html', form=form, navigation=True)
