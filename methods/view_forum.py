# -*- coding: utf-8 -*-

""" Вывод сообщений для страницы """

from flask import render_template
import flask

from appwiki.forms.message import CreateMessage

def get_word(url):
    return url.replace('_', ' ')

def view_forum(word):
    form = CreateMessage();
    messages = flask.g.database.get_messages_forum( word )
    if messages.count() == 0:
        messages = None
    return render_template( 'forum.html',
                            navigation = True,
                            messages = messages,
                            word = word,
                            title = get_word(word),
                            form = form
                          )
