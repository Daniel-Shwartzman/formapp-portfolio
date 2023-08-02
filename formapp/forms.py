from flask_wtf.form import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    SelectField,
    HiddenField
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