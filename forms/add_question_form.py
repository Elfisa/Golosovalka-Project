from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, DateTimeField, RadioField, FileField
from wtforms.validators import DataRequired
from db_data.__all_models import Group


class AddQuestionForm(FlaskForm):
    text = TextAreaField('Текст вопроса', validators=[DataRequired()])
    file = FileField('Добавить картинку вопроса')
    submit = SubmitField('Сохранить')
    add_answer = SubmitField('Добавить вариант ответа')
