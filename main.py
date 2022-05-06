import datetime
import flask_login
from flask import redirect, render_template, jsonify, make_response, Flask, session, url_for, Blueprint
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_restful import Api, Resource, abort
from db_data import db_session
from db_data.__all_models import User, Group, Vote, Question, Answer
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.add_vote_form import AddVoteForm
from forms.add_question_form import AddQuestionForm

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


@app.route('/create_vote', methods=['GET', 'POST'])
def create_vote():
    form = AddVoteForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        vote = Vote()
        vote.author_id = flask_login.current_user.id
        vote.title = form.title.data
        vote.description = form.description.data
        vote.stop_date = form.stop_date.data
        if form.groups.data != 'all':
            vote.groups.append(db_sess.query(Group).filter(Group.title == str(form.groups.data)).first())
        db_sess.add(vote)
        db_sess.commit()
        return redirect(url_for('vote_detail', vote_id=vote.id))
    return render_template('create_vote.html', form=form)


@app.route('/vote_detail/<vote_id>', methods=['GET', 'POST'])
def vote_detail(vote_id):
    db_sess = db_session.create_session()
    vote = db_sess.query(Vote).get(vote_id)
    groups = 'all' if not vote.groups else vote.groups.pop().title
    form = AddVoteForm(
        title=vote.title,
        description=vote.description,
        groups=groups,
        stop_date=vote.stop_date
    )
    if not vote.is_published:
        form.submit.label.text = 'Опубликовать'
    if form.validate_on_submit():
        vote.title = form.title.data
        vote.description = form.description.data
        vote.stop_date = form.stop_date.data
        if form.groups.data != 'all':
            vote.groups.append(db_sess.query(Group).filter(Group.title == str(form.groups.data)).first())
        db_sess.add(vote)
        db_sess.commit()
        if form.add_question.data:
            return redirect(url_for('create_question', vote_id=vote_id))
        return redirect(url_for('publish', vote_id=vote_id))
    return render_template('vote_detail.html', form=form)


@app.route('/create_question/<vote_id>', methods=['GET', 'POST'])
def create_question(vote_id):
    form = AddQuestionForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        question = Question()
        question.vote_id = vote_id
        question.text = form.text.data
        if form.file.data:
            img_name = datetime.datetime.now().strftime('%Y%b%d_%H%M%S')
            with open(f'static/imgs/{img_name}.png', 'wb') as output:
                output.write(form.file.data.read())
            question.icon = f'{img_name}.png'
        db_sess.add(question)
        db_sess.commit()
        return redirect(url_for('question_detail',
                                question_id=question.id,
                                question_icon=question.icon,
                                answers=question.answers))
    return render_template('create_question.html', form=form)


@app.route('/question_detail/<question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).get(question_id)
    form = AddQuestionForm(
        text=question.text
    )
    form.text.label.text = 'Добавить'
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        question.text = form.text.data
        if form.file.data:
            img_name = datetime.datetime.now().strftime('%Y%b%d_%H%M%S')
            with open(f'static/img/{img_name}.png', 'wb') as output:
                output.write(form.file.data.read())
            question.icon = f'{img_name}.png'
        db_sess.add(question)
        db_sess.commit()
        if form.add_answer.data:
            return redirect(url_for('create_answer', question_id=question_id))
        return redirect(url_for('vote_detail', vote_id=question.vote.id))
    return render_template('question_detail.html', form=form)


def publish(vote_id):
    db_sess = db_session.create_session()
    vote = db_sess.query(Vote).get(vote_id)
    vote.is_published = True
    return redirect(url_for('vote_detail', vote_id=vote_id))


def main():
    db_session.global_init('db/golosovalka.sqlite')
    app.run()


if __name__ == '__main__':
    main()
