# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for
import flask

from appwiki.forms.forms import InputForm

def get_url(word):
    url = str(word).strip()
    return url.replace(' ', '_')

def create():
    if request.form['action'] == 'create':
        form = InputForm(request.form)
        if form.validate():
            url = get_url(form.title.data)
            title = form.title.data.strip()
            text = form.text.data.strip()
            comment = form.comment.data.strip()
            flask.g.database.insert_page(url = url, title = title, text = text, comment = comment)
            return redirect(url_for('.view', word = url))
        else:
            return render_template('form.html', form = form, navigation = True)
    elif request.form['action'] == 'edit':
        form = InputForm(request.form)
        if form.validate():
            url = get_url(form.title.data)
            url_alt = form.url.data.strip()
            title = form.title.data.strip()
            text = form.text.data.strip()
            comment = form.comment.data.strip()
            flask.g.database.update_page(   url = url,
                                            url_alt = url_alt,
                                            title = title,
                                            text = text,
                                            comment = comment
                                        )
            return redirect(url_for('.view', word = url))
        else:
            pass
    elif request.form['action'] == 'history':
        pass
    else:
        pass
