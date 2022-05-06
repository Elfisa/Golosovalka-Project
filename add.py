from db_data import db_session
from db_data.__all_models import Group, User, Question, Answer, Vote
import datetime as dt

db_session.global_init(f'db/golosovalka.sqlite')
db_sess = db_session.create_session()


def add():
    user = User()
    user.email = 'student@email.com'
    user.set_password('student')
    user.group_id = Group().STUDENT
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.email = 'student2@email.com'
    user.set_password('student2')
    user.group_id = Group().STUDENT
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.email = 'parent@email.com'
    user.set_password('parent')
    user.group_id = Group().PARENT
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.email = 'teacher@email.com'
    user.set_password('teacher')
    user.group_id = Group().TEACHER
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.email = 'admin@email.com'
    user.set_password('admin')
    user.group_id = Group().STUDENT
    user.role = User().ADMIN
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.email = 'student_moderator@email.com'
    user.set_password('student_moderator')
    user.group_id = Group().STUDENT
    user.role = User().MODERATOR
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.email = 'teacher_moderator@email.com'
    user.set_password('teacher_moderator')
    user.group_id = Group().TEACHER
    user.role = User().MODERATOR
    db_sess.add(user)
    db_sess.commit()

    group = Group()
    group.title = group.STUDENT
    db_sess.add(group)
    db_sess.commit()
    group = Group()
    group.title = group.PARENT
    db_sess.add(group)
    db_sess.commit()
    group = Group()
    group.title = group.TEACHER
    db_sess.add(group)
    db_sess.commit()


# vote = Vote()
# vote.title = 'Голосование за самую симпатичную картинку.'
# vote.description = 'Картинка? Картинка.'
# author_id = 6
# db_sess.add(vote)
# db_sess.commit()

# for user in db_sess.query(User).filter((User.role == User.MODERATOR) | (User.role == User.ADMIN)):
#     print(user.id)
# for user in users:
#     user.icon = 'static/imgs/default.png'

# for user in db_sess.query(User).all():
#     user.role = int(user.role)
#     print([user.role])
#     db_sess.commit()
#     print([user.role])
#
# for group in db_sess.query(Group).all():
#     group.title = int(group.title)
#     db_sess.commit()
#
# db_sess.commit()

for vote in db_sess.query(Vote).all():
    print(vote.is_published)
