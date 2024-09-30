from project.extensions import db, bcrypt
from project.models.base import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
from project.models.posts import *

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    uid = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    posts = relationship('Post', backref=backref('user'))

    def __repr__(self) -> str:
        return f'<NAME: {self.first_name} {self.last_name}, EMAIL: {self.email}>'
    
    def get_id(self):
        return self.uid
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
    
    def check_password(self, password):
        return True if bcrypt.check_password_hash(password, self.password) else False


class AnonymousUser(UserMixin):
    uid = '10000000001'
    first_name = 'Anonymous'
    last_name = 'User'
    is_authenticated = False

    def __repr__(self) -> str:
        return f'<NAME: {self.first_name} {self.last_name}, EMAIL: {self.email}>'
    
    def get_id(self):
        return self.uid
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def set_password(self):
        pass
    
    def check_password(self):
        return True