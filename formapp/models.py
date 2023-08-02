from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from formapp.extensions import database as db

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    isOfficer = db.Column(db.Boolean, default=False, nullable=False)

    # Remove the cascade option from the assigned_tasks relationship
    assigned_tasks = db.relationship('Assignment', backref='user', lazy=True)

    @classmethod
    def assign_task(cls, user_id, task):
        assignment = Assignment(user_id=user_id, task=task)
        db.session.add(assignment)  # Add the assignment to the session
        db.session.commit()  # Commit the session to save the assignment


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task = db.Column(db.String(100), nullable=False)

    assigned_user = db.relationship('User', backref='assignments', lazy=True)

    @classmethod
    def delete_by_task(cls, task):
        assignment = cls.query.filter_by(task=task).first()
        if assignment:
            db.session.delete(assignment)
            db.session.commit()
            return True
        return False

    def __repr__(self):
        return f'<Assignment> (ID: {self.id}, User ID: {self.user_id}, Task: {self.task})'
