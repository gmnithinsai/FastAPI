from database import Base
from sqlalchemy import Integer, String, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable = False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates = 'blogs')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable = False)
    email = Column(String)
    password = Column(String)

    blogs = relationship('Blog', back_populates = 'creator')