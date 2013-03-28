# -*- coding: utf-8 -*-
""" Показ поста из истории """
from flask import render_template
import flask

import textile

def get_history_page( word, id ):
    post = flask.g.database.get_page_history( id )
    post['text'] = textile.textile( post['text'] )
    return render_template( 'history_post.html',
                            post = post,
                            navigation = True,
                            word = word)

