# -*- coding: utf-8 -*-
from wtforms import ValidationError, Form, TextField, validators, TextAreaField, SelectField, SubmitField, HiddenField

def validate_access_edit( form, field ):
    if len(field.data) == 0 or field.data is None:
        raise ValidationError(u'Поле права на доступ к файлу не может быть пустым')
    st = field.data
    error = False
    sk_begin = 0
    sk_end = 0
    for d in xrange(1, len(field.data)):
        if st[d] == '[':
            sk_begin = sk_begin + 1
        if st[d] == ']':
            sk_end = sk_end + 1

    if sk_begin != sk_end:
        raise ValidationError(u'Ошибка синтаксисса в параметрах прав на редактирование')


    if error is True:
        raise ValidationError(u'Ошибка синтаксисса в параметрах прав на редактирование')


    for i in xrange(0, len(field.data)):
        if st[i] == '=':
            if st[i+1] != '[':
                error = True
            if st[i-1] not in "qwertyuioasdfghjklzxcvbnm1234567890":
                error = True
        if st[i] == '[':
            for d in xrange(i, len(st)):
                if st[d] not in "reh,":
                    error = True
        if error is True:
            break

    if error is True:
        raise ValidationError(u'Ошибка синтаксисса в параметрах прав на редактирование')


class CreateDataForm(Form):
    title = TextField('Title', [validators.required(
        message=u'Поле название статьи не должно быть пустым')])#,validate_access_edit])
    text = TextAreaField('Text')
    submit = SubmitField(default=u"Сохранить")
    comment = TextField('Comment')
    tags = TextField('Tags')
    access = TextField('Access')
    access = TextField('Access', [validators.required(message=u'Вы не внесли права на правку и просмотр страницы'), ])
    access_show = TextField('AccessShow', [validators.required(message=u'Вы не внесли права на просмотр страницы')])
