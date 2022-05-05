from flaskfl_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

    submit = SubmitField('Войти')
