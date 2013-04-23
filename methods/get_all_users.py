# -*- coding: utf-8 -*-
""" Получаю список всех пользователей для установки их прав """

import flask

def get_all_users():
    users = flask.g.database.get_all_users()
    result = ""
    for user in users:
        id = user['_id']
        first_name = user['first_name']
        last_name = user['last_name']
        login = user['login']
        res = '<div class="user_data">' + last_name + " " + first_name + '</div>'
        res = '<div id="' + str(id) + '" login="' + login + '" >' + res + '</div>'
        result = result + res
    result = '<div style="display:none;" id="all_users">' + result + '</div>'
    return result
