import flask_login
from flask import redirect, render_template, jsonify, make_response, Flask, session
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_restful import Api, Resource, abort
from db_data import db_session
from db_data.__all_models import User, Group, Vote, Question, Answer
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.vote_form import VoteForm
from forms.question_form import QuestionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        group = db_sess.query(Group).filter(Group.title == form.group.data)
        user.group_id = group.id
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/')
def run():
    db_sess = db_session.create_session()
    return render_template('index.html', votes=db_sess.query(Vote).all())


@app.route('/create/<vote_id>', methods=['GET', 'POST'])
def create(vote_id):
    db_sess = db_session.create_session()
    form = VoteForm()
    if form.validate_on_submit():
        print(form.stop_date.data)
        print(vote_id)
        vote = db_sess.query(Vote).get(vote_id)
        vote.title = form.title.data
        vote.description = form.description.data
        db_sess.commit()
        if form.add.data:
            question = Question()
            db_sess.add(question)
            vote.questions.append(question)
            db_sess.commit()
            return redirect(f'/create/{vote.id}/add/{question.id}')
        return redirect('/')
    if vote_id == 'new':
        vote = Vote()
        db_sess.add(vote)
        db_sess.commit()
        vote_id = vote.id
    return render_template('create.html', form=form, vote_id=vote_id)


@app.route('/create/<vote_id>/add_question/<question_id>', methods=['GET', 'POST'])
def add_question(vote_id, question_id):
    form = QuestionForm()
    return render_template('add_question.html', form=form)


def main():
    db_session.global_init('db/golosovalka.sqlite')
    app.run()


if __name__ == '__main__':
    main()
