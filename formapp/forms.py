from flask_wtf.form import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    SelectField,
    HiddenField,
    DateField
)

from wtforms.validators import (
    DataRequired,
    Length
)
from formapp.validators import Unique
from formapp.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 128)])
    isOfficer = BooleanField('Are you an officer?')
    submit = SubmitField('Register')

class AssignTaskForm(FlaskForm):
    user = SelectField('Select User', validators=[DataRequired()])
    task = TextAreaField('Task', validators=[DataRequired(), Length(1, 100)])
    submit = SubmitField('Assign Task')

class FlyingForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=30)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Submit')