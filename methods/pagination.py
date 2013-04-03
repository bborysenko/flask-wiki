# -*- coding: utf-8 -*-
""" Пагинация страницы """


def pagination(count=0, size=0, numer=0, url=None,):
    # count - колличество страниц, size - колличество постов на страницы,
    # numer - номер страницы

    # высчитываю сколько страниц будет всего
    count_page = count / size
    if count % size != 0:
        count_page = count_page + 2
    else:
        count_page = count_page + 1

    if numer == 0 or numer is None:
        numer = 1

    pag = """ """
    for d in xrange(1, count_page):
        style = ''
        if int(d) == int(numer):
            style = ' style="font-size:14px;color:#f00;margin-left:15px;margin-right:15px;" '
        else:
            style = ' style="font-size:14px;color:#00f;margin-left:15px;margin-right:15px;" '

        link_page = '<span><a' + style + 'href="' + \
            url + str(d) + '">' + str(d) + '</a></span>'
        pag = pag + link_page

    pag = '<div style="height:30px;text-align:center;">' + pag + '</div>'

    return pag
