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
    assignments = db.relationship('Assignment', back_populates='assigned_user', viewonly=True)

    @classmethod
    def assign_task(cls, user_id, task):
        assignment = Assignment(user_id=user_id, task=task)
        db.session.add(assignment)  # Add the assignment to the session
        db.session.commit()  # Commit the session to save the assignment


    def get_user_by_username(self, cls, username):
        return cls.query.filter_by(username=username).first()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_officers(cls):
        return cls.query.filter_by(isOfficer=True).all()
    
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
    assigned_user = db.relationship('User', back_populates='assignments', viewonly=True)

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

class Flying(db.Model):
    __tablename__ = 'flying'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.String(30), nullable=False)
    end_date = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    isConfirmed = db.Column(db.Boolean, default=False, nullable=False)

    @classmethod
    def confirm(cls, id):
        flying = cls.query.get(id)
        if flying:
            # Update the confirmation status and commit changes
            flying.isConfirmed = True
            db.session.commit()
            return True
        return False
    
    @classmethod
    def create_flying(cls, full_name, start_date, end_date, location):
        flying = cls(full_name=full_name, start_date=start_date, end_date=end_date, location=location)
        db.session.add(flying)
        db.session.commit()

    @classmethod
    def not_confirm(cls, id):
        flying = cls.query.get(id)
        if flying:
            # Update the confirmation status and commit changes
            flying.isConfirmed = False
            db.session.commit()
            return True
        return False

    @classmethod
    def delete(cls, id):
        flying = cls.query.get(id)
        if flying:
            # Delete the flying record and commit changes
            db.session.delete(flying)
            db.session.commit()
            return True
        return False

    def __repr__(self):
        return (
    f'<Flying> (ID: {self.id}, Full Name: {self.full_name}, '
    f'Start Date: {self.start_date}, End Date: {self.end_date}, '
    f'Location: {self.location})'
)

class Driving(db.Model):
    __tablename__ = 'driving'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(30), nullable=False)
    destination = db.Column(db.String(30), nullable=False)
    commanding_officer = db.Column(db.String(30), nullable=False)
    isConfirmed = db.Column(db.Boolean, default=False, nullable=False)

    @classmethod
    def confirm(cls, id):
        driving = cls.query.filter_by(id=id).first()
        if driving:
            driving.isConfirmed = True
            db.session.commit()
            return True
        return False
    
    @classmethod
    def create_driver(cls, full_name, destination, commanding_officer):
        driving = cls(full_name=full_name, destination=destination, commanding_officer=commanding_officer)
        db.session.add(driving)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def delete_by_driver(cls, full_name):
        driving = cls.query.filter_by(full_name=full_name).first()
        if driving:
            db.session.delete(driving)
            db.session.commit()
            return True
        return False

    def __repr__(self):
        return (
    f'<Driving> (ID: {self.id}, Full Name: {self.full_name}, '
    f'Destination: {self.destination}, Commanding Officer: {self.commanding_officer})'
)

