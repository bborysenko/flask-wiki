# -*- coding: utf-8 -*-0
from wtforms import Form, TextField, validators, TextAreaField, SelectField, SubmitField, HiddenField

class EditDataForm( Form ):
    title = TextField( 'Title', [ validators.required( message = u'Поле название статьи не должно быть пустым' ) ] )
    text = TextAreaField('Text')
    submit = SubmitField(default = u"Сохранить")
    comment = TextField('Comment')
    tags = TextField('Tags')
    url = HiddenField('url')
    access = TextField('Access')
