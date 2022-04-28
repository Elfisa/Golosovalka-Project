from db_data import db_session
from db_data.__all_models import User, Group

db_session.global_init(f'db/golosovalka.sqlite')
# user = User()
# user.email = 'email@email.com'
# user.set_password('password')
# db_sess = db_session.create_session()
# db_sess.add(user)
# db_sess.commit()
group = Group()
group.title = group.STUDENT
db_sess = db_session.create_session()
db_sess.add(group)
db_sess.commit()
group = Group()
group.title = group.PARENT
db_sess = db_session.create_session()
db_sess.add(group)
db_sess.commit()
group = Group()
group.title = group.TEACHER
db_sess = db_session.create_session()
db_sess.add(group)
db_sess.commit()
