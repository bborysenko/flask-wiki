# -*- coding: utf-8 -*-
""" Выборка последних статей """

from flask import render_template, g

def get_pages_latter( num = None ):
    return render_template('latter.html')

