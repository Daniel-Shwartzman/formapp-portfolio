from flask_wtf.form import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired,
    Length
)
from formapp.validators import Unique
from formapp.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(1, 30), Unique(User, User.username, message='Username already exists choose another.')]
    )      
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 128)])
    submit = SubmitField('Continue')

class RegisterForm(FlaskForm):

    username = StringField('Username', 
        validators=[DataRequired(), Length(1, 30), Unique(User, User.username, message='Username already exists choose another.')]
    )      
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 128)])
    isOfficer = BooleanField('Officer', validators=[DataRequired()])
    submit = SubmitField('Continue')