from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, DateTimeField, RadioField
from wtforms.validators import DataRequired
from db_data.__all_models import Group


class CreateVoteForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    stop_date = DateTimeField('Дата и время окончания (дд/мм/гг часы:минуты)',
                              format='%d/%m/%y %H:%M', validators=[DataRequired()])
    groups = RadioField('Для кого это голосование?',
                        choices=[(None, 'Для всех'), (Group.STUDENT, 'Для учеников'),
                                 (Group.PARENT, 'Для родителей'), (Group.TEACHER, 'Для учителей')])
    submit = SubmitField('Сохранить')
    short_answer = SubmitField('Вопрос с кратким ответом')
    radio_answer = SubmitField('Вопрос с выбором ответа')
