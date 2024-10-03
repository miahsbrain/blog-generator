from project.models.base import BaseModel
from project.extensions.dependencies import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

class Post(BaseModel):
    __tablename__ = 'posts'
    pid = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(String, ForeignKey('users.uid'), nullable=False)
    links = relationship('Link', backref=backref('post'))

    def __repr__(self):
        return f'<ID: {self.pid}, TITLE: {self.title}>'
    
class Link(BaseModel):
    __tablename__ = 'links'
    lid = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    link = Column(Text, nullable=True)
    post_id = Column(ForeignKey('posts.pid'), nullable=True)

    def __repr__(self):
        return f'<ID: {self.link}>'