# -*- coding: utf-8 -*-
from flask import render_template, request
import flask
import textile

from appwiki.forms.forms import InputForm

def _get_url(word):
	url = word.strip()
	return url.replace(' ', '_')

def view(word = None):
	action = request.args.get('action')
	if word is None and action is None:
		return render_template('general.html')
	else:
		if action is None:
			return _get_page(word)
		else:
			if action == 'create':
				return _get_form_create()
			elif action == 'edit':
				return _get_form_edit(word)
			elif action == 'random':
				# отдать рандомную статью
				pass

def _get_page(word):
	url = _get_url(word)
	page = flask.g.database.get_page(url)
	if page is None:
            return _get_form_create()
	else:
            page['text'] = textile.textile(page['text'])
            return render_template(
					    'page.html',
                        page = page,
					    navigation = True,
                        word = url
				    )

def _get_form_create():
    form = InputForm()
    form.action.data = u"create"
    return  render_template('form.html', form = form)

def _get_form_edit(word):
    form = InputForm()
    url = _get_url(word)
    page = flask.g.database.get_page(url)

    if page is None:
        form.url.data = word
        form.action.data = u"edit"
        return render_template('form', form = form)
    else:
        form.submit.data = u"Изменить"
        form.title.data = page['title']
        form.text.data = page['text']
        form.action.data = u"edit"
        form.url.data = page['url']
        form.submit.data = u"Сохранить"
        return render_template('form.html', form = form, navigation = True, word = url)





