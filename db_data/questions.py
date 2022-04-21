import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import datetime as dt


class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.Text)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    settings = sqlalchemy.Column(sqlalchemy.JSON)  # БЕЗ ПОНЯТИЯ КАКОЙ ДОЛЖЕН БЫТЬ ТИП

    vote_id = orm.relation(sqlalchemy.Integer, sqlalchemy.ForeignKey('votes.id'))
    vote = orm.relation('Vote')  # nahuya?

    answers = orm.relation('Answer', back_populates='question')
