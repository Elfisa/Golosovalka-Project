import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import datetime as dt

votes_to_groups = sqlalchemy.Table(
    'votes_to_groups',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('votes', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('votes.id')),
    sqlalchemy.Column('groups', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('groups.id'))
)


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    token = sqlalchemy.Column(sqlalchemy.String, default=)

    users = orm.relation('User', back_populates='group')
