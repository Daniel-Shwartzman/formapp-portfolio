"""
This module initializes various extensions for the Form app.
"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5

# csrf protection
csrf = CSRFProtect()

# database
database = SQLAlchemy()

# A bootstrap5 class for styling client sidpythe.
bootstrap = Bootstrap5()

# login manager
login_manager = LoginManager()
