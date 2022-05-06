import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import datetime as dt


users_to_votes = sqlalchemy.Table(
    'users_to_votes',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('votes', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('votes.id'))
)


class Vote(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'votes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    icon = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=dt.datetime.now())
    stop_date = sqlalchemy.Column(sqlalchemy.DateTime, default=dt.datetime.now())
    is_published = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_hidden = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    author = orm.relation('User')

    voters = orm.relation("User",  # votes.voters.append(current_user)
                          secondary="users_to_votes",
                          back_populates="passed_votes")

    groups = orm.relation("Group",
                          secondary="votes_to_groups",
                          back_populates="votes")

    questions = orm.relation('Question', back_populates='vote')

    @property
    def formatted_start(self):
        return self.start_date.strftime("%d/%m/%y %H:%M")

    @property
    def formatted_stop(self):
        return self.stop_date.strftime("%d/%m/%y %H:%M")
