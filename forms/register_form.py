from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField, RadioField
from wtforms.validators import DataRequired
from db_data.__all_models import Group


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    group = RadioField('Вы...', choices=[(Group.STUDENT, 'Ученик'), (Group.PARENT, 'Родитель')])

    submit = SubmitField('Зарегистрироваться')
