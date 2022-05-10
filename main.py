import datetime
import os
import time
from PIL import Image
from flask import redirect, render_template, Flask, url_for, Blueprint, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from db_data import db_session
from db_data.__all_models import User, Group, Vote, Question, Answer
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.add_vote_form import AddVoteForm
from forms.add_question_form import AddQuestionForm
from forms.add_answer_form import AddAnswerForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'imgs'
login_manager = LoginManager()
login_manager.init_app(app)

blueprint = Blueprint(
    'main',
    __name__,
    template_folder='templates'
)


def resize(file_path, max_size=300, max_height=False):
    img = Image.open(file_path)
    width, height = img.size
    _max_size = max(width, height)
    if max_height:
        img = img.resize(
            (round(width / max_size),
             round(height / max_size)),
            Image.ANTIALIAS
        )
    elif _max_size > max_size:
        img = img.resize(
            (round(width / _max_size * max_size),
             round(height / _max_size * max_size)),
            Image.ANTIALIAS
        )
        img.save(file_path)


def get_image(form):
    img = form.img.data
    f_name = secure_filename(img.filename)
    if '.' not in f_name:
        f_name = f'unknown.{f_name}'
    i = 0
    while os.path.exists(os.path.join('static', 'imgs', f_name)):
        f_name = f'{i}{f_name}'
        i += 1
    path_file = os.path.join('static', 'imgs', f_name)
    img.save(path_file)
    resize(path_file)
    return f_name


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
                               form=form,
                               title='Авторизация')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html',
                                   title='Регистрация',
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
@app.route('/active_votes')
def active_votes():
    db_sess = db_session.create_session()
    return render_template('votes_list/active_votes.html',
                           title='Активные голосования',
                           votes=db_sess.query(Vote).filter(Vote.is_published,
                                                            ~Vote.is_hidden,
                                                            Vote.is_finished != True).all())


@app.route('/finished_votes')
def finished_votes():
    db_sess = db_session.create_session()
    return render_template('votes_list/finished_votes.html',
                           title='Результаты голосований',
                           votes=db_sess.query(Vote).filter(Vote.is_published,
                                                            ~Vote.is_hidden,
                                                            Vote.is_finished == True).all())


@app.route('/hidden_votes')
def hidden_votes():
    db_sess = db_session.create_session()
    return render_template('votes_list/hidden_votes.html',
                           title='Скрытые голосования',
                           votes=db_sess.query(Vote).filter(Vote.is_hidden).all())


@app.route('/draft_votes')
def draft_votes():
    db_sess = db_session.create_session()
    return render_template('votes_list/draft_votes.html',
                           title='Черновики',
                           votes=db_sess.query(Vote).filter(~Vote.is_published,
                                                            Vote.author_id == current_user.id).all())


@app.route('/my_votes')
def my_votes():
    db_sess = db_session.create_session()
    return render_template('votes_list/my_votes.html',
                           title='Мои активные голосования',
                           votes=db_sess.query(Vote).filter(Vote.is_published,
                                                            Vote.author_id == current_user.id).all())


@app.route('/create_vote', methods=['GET', 'POST'])
def create_vote():
    form = AddVoteForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        vote = Vote(
            author_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            stop_date=form.stop_date.data
        )
        db_sess.merge(current_user)
        if form.groups.data != 'all':
            vote.groups.append(db_sess.query(Group).filter(Group.title == str(form.groups.data)).first())
        db_sess.add(vote)
        db_sess.commit()
        return redirect(url_for('vote_detail', vote_id=vote.id))
    return render_template('create_and_detail/create_vote.html',
                           title='Создание голосования',
                           form=form,
                           vote=None)


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
    if vote.is_hidden:
        form.hide.label.text = 'Сделать активным'
    if form.validate_on_submit():
        vote.title = form.title.data
        vote.description = form.description.data
        vote.stop_date = form.stop_date.data
        if form.groups.data != 'all':
            vote.groups.append(db_sess.query(Group).filter(Group.title == str(form.groups.data)).first())
        db_sess.commit()
        if form.add_question.data:
            return redirect(url_for('create_question', vote_id=vote_id))
        if form.publish.data:
            return redirect(url_for('publish', vote_id=vote_id))
        if form.hide.data:
            vote.is_hidden = not vote.is_hidden
            db_sess.commit()
            return redirect(url_for('vote_detail', vote_id=vote_id))
        if form.delete.data:
            db_sess.delete(vote)
            time.sleep(7)
            db_sess.commit()
            return redirect(url_for('active_votes'))
    return render_template('create_and_detail/vote_detail.html',
                           title='Детали голосования',
                           form=form,
                           vote=vote)


@app.route('/create_question/<vote_id>', methods=['GET', 'POST'])
def create_question(vote_id):
    form = AddQuestionForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        question = Question(
            vote_id=vote_id,
            text=form.text.data
        )
        db_sess.add(question)
        if form.img.data:
            f_name = get_image(form)
            question.icon = f_name
        db_sess.commit()
        return redirect(url_for('question_detail',
                                question_id=question.id,
                                question_icon=question.icon,
                                answers=question.answers))
    return render_template('create_and_detail/create_question_or_answer.html',
                           title='Добавление вопроса',
                           form=form,
                           question=None)


@app.route('/question_detail/<question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).get(question_id)
    form = AddQuestionForm(
        text=question.text
    )
    form.submit.label.text = 'Готово'
    if form.validate_on_submit():
        question.text = form.text.data
        db_sess = db_session.create_session()
        if form.img.data:
            f_name = get_image(form)
            question.icon = f_name
        db_sess.commit()
        if form.add_answer.data:
            question.type = Question.RADIO
            return redirect(url_for('create_answer', question_id=question_id))
        if not question.type:
            question.type = Question.SHORT
        return redirect(url_for('vote_detail', vote_id=question.vote.id))
    return render_template('create_and_detail/question_detail.html',
                           title='Детали вопроса',
                           form=form,
                           question=question)


@app.route('/create_answer/<question_id>', methods=['GET', 'POST'])
def create_answer(question_id):
    form = AddAnswerForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        answer = Answer(
            question_id=question_id,
            text=form.text.data
        )
        if form.img.data:
            f_name = get_image(form)
            answer.icon = f_name
        db_sess.add(answer)
        db_sess.commit()
        return redirect(url_for('question_detail', question_id=question_id))
    return render_template('create_and_detail/create_question_or_answer.html',
                           title='Добавление варианта ответа',
                           form=form,
                           question=None)


@app.route('/publish/<vote_id>')
def publish(vote_id):
    db_sess = db_session.create_session()
    vote = db_sess.query(Vote).get(vote_id)
    vote.start_date = datetime.datetime.now()
    vote.is_published = True
    time.sleep(6)
    db_sess.commit()
    return redirect(url_for('vote_detail', vote_id=vote_id))


@app.route('/users_list')
def users_list():
    db_sess = db_session.create_session()
    users = db_sess.query(User).order_by(User.email).all()
    return render_template('users_list.html',
                           title='Список пользователей',
                           users=users,
                           object=User)


@app.route('/change_role/<user_id>/<new_role>')
def change_role(user_id, new_role):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    user.role = new_role
    db_sess.commit()
    return redirect(url_for('users_list'))


@app.route('/voting/<vote_id>', methods=['GET', 'POST'])
def voting(vote_id):
    db_sess = db_session.create_session()
    vote = db_sess.query(Vote).get(vote_id)
    if request.method == 'GET':
        return render_template('voting.html',
                               title=vote.title,
                               vote=vote)
    if request.method == 'POST':
        db_sess.close()
        db_sess = db_session.create_session()
        vote = db_sess.query(Vote).get(vote_id)
        outer_loop = 0
        current_user.passed_votes.append(vote)
        for question in vote.questions:
            if question.answers:
                answer_id = request.form[f'{outer_loop}']
                answer = db_sess.query(Answer).get(answer_id)
                answer.voters.append(current_user)
                db_sess.merge(current_user)
            else:
                answer = request.form[f'{outer_loop}']
                question.answer = answer
            outer_loop += 1
        db_sess.merge(current_user)
        return redirect(url_for('active_votes'))


def main():
    db_session.global_init('db/golosovalka.sqlite')
    app.run()


if __name__ == '__main__':
    main()
