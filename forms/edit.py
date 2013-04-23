# -*- coding: utf-8 -*-0
from wtforms import widgets, Form, SelectField, TextField, validators, BooleanField, TextAreaField, SubmitField, HiddenField


class EditDataForm(Form):
#    title = TextField('Title', [validators.required(
#        message=u'Поле название статьи не должно быть пустым')])
    text = TextAreaField('Text')
    submit = SubmitField(default=u"Сохранить")
    comment = TextField('Comment')
#    tags = widgets.ListWidget(html_tag = u'ul')
#    tags = SelectField('Tags', choices = [])
    tags = TextField('Tags')
    url = HiddenField('url')
    access = TextField('Access', [validators.required(message=u'Вы не внесли права  на правку страницы')])
    access_show = TextField('AccessShow', [validators.required(message=u'Вы не внесли права на просмотр страницы')])
    active = BooleanField('Active')

# Форма для заглавной страницы
class ServiceGeneralForm(Form):
    title = TextField('Title', [validators.required(message=u'Заголовок должен быть заполнен')])
    text = TextAreaField('Text')

class ServiceLeftMenuForm(Form):
    text = TextAreaField('Text')
