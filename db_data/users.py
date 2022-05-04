import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    USER = 1
    ADMIN = 2
    MODERATOR = 3

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    icon = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.Integer, default=USER)

    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id'))
    group = orm.relation('Group')

    created_votes = orm.relation('Vote', back_populates='author')
    passed_votes = orm.relation("Vote",
                                secondary="users_to_votes",
                                back_populates="voters")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def is_admin(self):
        return int(self.role) == self.ADMIN

    @property
    def is_moderator(self):
        return int(self.role) == self.MODERATOR
