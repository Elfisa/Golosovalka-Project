import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Answer(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'votings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    icon = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    question_id = orm.relation(sqlalchemy.Integer, sqlalchemy.ForeignKey('questions.id'))
    question = orm.relation('Question')
