# -*- coding: utf-8 -*-
""" Выборка статей с последними правками """

from flask import render_template, g
from appwiki.methods.access import access_f
from flask.ext.login import current_user

def view_pages_latedit(num=None):
    data = g.database.get_latedit_page()
    pages = []
    key = False
    if current_user.is_authenticated():
        if current_user.is_admin():
            pages = data
            key = True
    if key is False:
        for d in data:
            access = access_f(d['access'], current_user)
            if access is True:
                pages.append(d)

    return render_template('latedit.html', pages = pages)
