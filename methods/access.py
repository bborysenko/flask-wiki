# -*- coding: utf-8 -*-

# from src.admin.sadmin import SADMIN
# import src.admin
""" Проверка на полномочия пользователя вносить изменение в статью """


def access_f(str_access, current_user):
    access_edit = False

    list_access = str_access.split(',')
    if current_user.is_authenticated() is False:
        for d in list_access:
            if d.strip().lower() == 'all':
                return True


    for d in list_access:
        d = d.strip().lower()
        if d.find('!') == -1:
            # разрешение
            if d == 'all':
                access_edit = True
            else:
                if d == current_user.login.lower():
                    access_edit = True
                    break
        else:
            # запрет
            d = d[1:]
            if d == current_user.login.lower():
                access_edit = False
                break
    # админу все можно :)
#   if access_edit is False:
#        for item in SADMIN:
#            if item == current_user.login.lower():
#                access_edit = True
#    access_edit2.x
    return access_edit
