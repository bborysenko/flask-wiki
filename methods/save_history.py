# -*- coding: utf-8 -*-
from flask import request, redirect, url_for
import flask


def save_history(word):
    page_id = request.form['history']
    flask.g.database.set_activity_history(word, page_id)
    return redirect(url_for('.view', word=word))
