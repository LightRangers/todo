from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, )
from models.db import Base, DBSession
from sqlalchemy.orm import relationship

session = DBSession()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    createtime = Column(DateTime, default=datetime.now)
    email = Column(String(80))


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    # 建立外键关系
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref='posts', uselist=False, cascade='all')


def register(username, password):
    s = DBSession()
    s.add(User(name=username, password=password))
    s.commit()


if __name__ == '__main__':
    Base.metadata.create_all()
