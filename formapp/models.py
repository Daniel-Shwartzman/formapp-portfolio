from flask import url_for
from flask_login.mixins import UserMixin
from flask_login import LoginManager
from werkzeug.security import(
    generate_password_hash,
    check_password_hash
)
from formapp.extensions import database as db

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    isOfficer = db.Column(db.Boolean, default=False, nullable=False)

    # profile = db.Relationship('Profile', backref='user', cascade='save-update, merge, delete')


    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_officer(cls):
        return cls.query.filter_by(isOfficer=True).first()

    def __repr__(self):
        return '<User> {}'.format(self.username)
    
class Assignment(db.Model):
    __tablename__ = 'assignment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    task = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Assignment> (ID: {self.id}, Username: {self.username}, Task: {self.task})'