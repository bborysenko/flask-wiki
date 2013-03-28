# -*- coding: utf-8 -*-
from wtforms import Form, TextField, validators, TextAreaField, SelectField, SubmitField, HiddenField

class CreateDataForm( Form ):
    title = TextField( 'Title', [ validators.required( message = u'Поле название статьи не должно быть пустым' ) ] )
    text = TextAreaField( 'Text' )
    submit = SubmitField( default = u"Сохранить" )
    comment = TextField( 'Comment' )
    tags = TextField( 'Tags' )
    access = TextField('Access')
