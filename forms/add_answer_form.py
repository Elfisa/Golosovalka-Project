from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, StringField, TextAreaField, DateTimeField, RadioField, FileField
from wtforms.validators import DataRequired
from db_data.__all_models import Group


class AddAnswerForm(FlaskForm):
    text = TextAreaField('Текст вопроса', validators=[DataRequired()])
    img = FileField('Добавить картинку вопроса', validators=[FileAllowed(['jpg', 'png'], 'Только изображения!')])
    submit = SubmitField('Сохранить')
