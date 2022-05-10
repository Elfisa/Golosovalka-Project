from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, DateTimeField, RadioField
from wtforms.validators import DataRequired
from db_data.__all_models import Group


class AddVoteForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    stop_date = DateTimeField('Дата и время окончания (дд/мм/гг часы:минуты)',
                              format='%d/%m/%y %H:%M', validators=[DataRequired()])
    groups = RadioField('Это голосование для...',
                        choices=[('all', 'всех'), (Group.STUDENT, 'учеников'),
                                 (Group.PARENT, 'родителей'), (Group.TEACHER, 'учителей')])
    save = SubmitField('Сохранить изменения')
    publish = SubmitField('Опубликовать')
    hide = SubmitField('Скрыть')
    delete = SubmitField('Удалить')
    add_question = SubmitField('Добавить вопрос')
