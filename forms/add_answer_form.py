from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, StringField, TextAreaField, DateTimeField, RadioField, FileField
from wtforms.validators import DataRequired


class AddAnswerForm(FlaskForm):
    text = TextAreaField('Текст варианта ответа')
    img = FileField('Добавить картинку', validators=[FileAllowed(['jpg', 'png'], 'Только изображения!')])
    submit = SubmitField('Сохранить')
