import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


user_to_voting = sqlalchemy.Table(
    'user_to_voting',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('voting', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('voting.id'))
)


class Voting(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'voting'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    title = sqlalchemy.Column(sqlalchemy.String)
    icon = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('User')

    @property
    def is_admin(self):
        return True if self.role == 'admin' else False
