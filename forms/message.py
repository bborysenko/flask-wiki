 # -*- coding: utf-8 -*-0
from wtforms import Form, TextField, validators, TextAreaField, SelectField, SubmitField, HiddenField


class CreateMessage(Form):
    text = TextAreaField('Text', [validators.required(
        message=u'Введите текст сообщения')])
    submit = SubmitField(default=u"Сохранить")
