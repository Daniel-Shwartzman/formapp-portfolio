from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import migrate

# csrf protection
csrf = CSRFProtect()

# database
database = SQLAlchemy()

# login manager
login_manager = LoginManager()

# migration
migrate = migrate(command='db')