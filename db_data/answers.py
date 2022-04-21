import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import datetime as dt


class Voting(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'votings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    icon = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    question_id = orm.relation(sqlalchemy.Integer, sqlalchemy.ForeignKey('questions.id'))
    question = orm.relation('Question')  # nahuya?
