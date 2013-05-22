# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for
import flask

from flask.ext.login import current_user

from appwiki.forms.message import CreateMessage


def get_url(word):
    return word.strip().replace(' ', '_')


def get_word(url):
    return url.strip().replace('_', ' ')


def save_message(word):
    form = CreateMessage(request.form)
    if form.validate() is True:
        user_name = current_user.login
        text = form.text.data.strip()

        flask.g.database.set_message_forum(text=text,
                                           user_name=user_name,
                                           url=get_url(word)
                                           )
        return redirect(url_for('.view_forum', word=get_url(word)))
    else:
        return render_template('forum.html',
                               navigation=True,
                               form=form,
                               word=get_url(word),
                               title=get_word(word)
                               )
