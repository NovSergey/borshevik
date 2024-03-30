
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

class Polygons(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'polygons'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    picture = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    coords = sqlalchemy.Column(sqlalchemy.String(1000), unique=False, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Integer)
    def __repr__(self):
        return f"USER - {self.id}, {self.coords}"