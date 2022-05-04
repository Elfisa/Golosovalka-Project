from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired


class VoteForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    stop_date = DateTimeField('Выберите дату и время окончания', format='%d/%m/%y %H:%M', validators=[DataRequired()])
    add = SubmitField('Добавить вопрос')
    submit = SubmitField('Сохранить')
