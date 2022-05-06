import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from uuid import uuid1

votes_to_groups = sqlalchemy.Table(
    'votes_to_groups',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('votes',
                      sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('votes.id')),
    sqlalchemy.Column('groups',
                      sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('groups.id'))
)


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    STUDENT = 1
    PARENT = 2
    TEACHER = 3

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    token = sqlalchemy.Column(sqlalchemy.String, default=str(uuid1()))

    votes = orm.relation("Vote",
                         secondary="votes_to_groups",
                         back_populates="groups")

    users = orm.relation('User', back_populates='group')

    @property
    def is_student(self):
        return int(self.title) == self.STUDENT

    @property
    def is_parent(self):
        return int(self.title) == self.PARENT

    @property
    def is_teacher(self):
        return int(self.title) == self.TEACHER
