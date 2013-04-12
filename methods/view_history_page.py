# -*- coding: utf-8 -*-
""" Показ поста из истории """
from flask import render_template
import flask

import markdown2


def view_history_page(word, id):
    post = flask.g.database.get_page_history(word, id)
    if post is not None:
        post['text'] = markdown2.markdown(post['text'])
    return render_template('history_post.html',
                           post=post,
                           navigation=True,
                           word=word)
