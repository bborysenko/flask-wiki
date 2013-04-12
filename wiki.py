# -*- coding: utf-8 -*-
from flask import Blueprint, current_app
import flask

from flask.ext.login import LoginManager, UserMixin, AnonymousUser, login_user, logout_user, current_user, login_required, make_secure_token


from methods.view import view
from methods.save_edit import save_edit
from methods.view_form_edit import view_form_edit
from methods.view_form_history import view_form_history
from methods.save_history import save_history
from methods.view_history_page import view_history_page
from methods.view_find_tag import view_find_tag
from methods.view_all_pages import view_all_pages
from methods.find_pages import find_pages
from methods.view_forum import view_forum
from methods.save_message import save_message
from methods.view_alphabet import view_alphabet
from methods.view_pages_favorites import view_pages_favorites
from methods.view_pages_latedit import view_pages_latedit
from methods.view_pages_latter import view_pages_latter

from database.database import get_database_object

#current_app.config['hello'] = 'hello'

wiki = Blueprint('appwiki', __name__,
                 template_folder='templates', static_folder='static')



@wiki.before_app_request
def before_app_request():
    flask.g.database = get_database_object('psql')
# Обсуждения
wiki.add_url_rule('/<word>/forum', methods=['GET', ], view_func=view_forum)
wiki.add_url_rule('/<word>/forum', methods=[
                  'POST', ], view_func=save_message)


# Поиск
wiki.add_url_rule('/find', methods=['POST', ], view_func=find_pages)

# Вывести все статьи
wiki.add_url_rule('/all/<page_num>', methods=[
                  'GET', ], view_func=view_all_pages)
wiki.add_url_rule('/all', methods=['GET', ], view_func=view_all_pages)


wiki.add_url_rule('/alphabet/<letter>', methods=[
                  'GET', ], view_func=view_alphabet)
wiki.add_url_rule('/alphabet', methods=['GET'], view_func=view_alphabet)

# Поиск по тегам
wiki.add_url_rule('/tags/<tags>', methods=[
                  'GET', ], view_func=view_find_tag)

# Показ статьи
wiki.add_url_rule('/<word>', methods=['GET', ], view_func=view)
wiki.add_url_rule('/', methods=['GET', ], view_func=view)

# Получить форму для создания/редактрирования
wiki.add_url_rule('/<word>/edit', methods=[
                  'GET', ], view_func=view_form_edit)
# Правка статьи
wiki.add_url_rule('/<word>/edit', methods=['POST', ], view_func=save_edit)

# Получить форму для истории
wiki.add_url_rule('/<word>/history', methods=[
                  'GET', ], view_func=view_form_history)
# Правка истории
wiki.add_url_rule('/<word>/history', methods=[
                  'POST', ], view_func=save_history)
# Показ отдельного поста из истории
wiki.add_url_rule('/<word>/history/<id>', methods=[
                  'GET', ], view_func=view_history_page)

# Выборка избранных статей
wiki.add_url_rule('/favorites/<num>', methods=[
                  'GET', ], view_func=view_pages_favorites)
wiki.add_url_rule('/favorites', methods=[
                  'GET', ], view_func=view_pages_favorites)

# Выборка статей для которых проводились правки
wiki.add_url_rule('/latedit/<num>', methods=[
                  'GET', ], view_func=view_pages_latedit)
wiki.add_url_rule('/latedit', methods=[
                  'GET', ], view_func=view_pages_latedit)

# Выборка последних статей
wiki.add_url_rule('/latter/<num>', methods=[
                  'GET', ], view_func=view_pages_latter)
wiki.add_url_rule('/latter', methods=['GET', ], view_func=view_pages_latter)
