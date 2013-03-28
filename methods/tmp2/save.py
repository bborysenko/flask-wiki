# -*- coding: utf-8 -*-
import flask
from flask import request, render_template
from appwiki.forms.create import FormCreate

def save( word = None ):
    if request.form['url'] is not None:
        # Редактирование
        pass
    else:
        # Новая запись
        form = FromCreate( request.form )
        flask.g.database.insert_page(  )

