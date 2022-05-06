import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'

    SHORT = 1
    RADIO = 2
    CHECKBOX = 3

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.Text)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    icon = sqlalchemy.Column(sqlalchemy.String)
    settings = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)

    vote_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('votes.id'))
    vote = orm.relation('Vote')

    answers = orm.relation('Answer', back_populates='question')
