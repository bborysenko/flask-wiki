# -*- coding: utf-8 -*-
""" Выборка статей с последними правками """

from flask import render_template, g

def get_pages_latedit( num = None ):
    return render_template('latedit.html')
