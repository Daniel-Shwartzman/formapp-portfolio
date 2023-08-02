from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5

# csrf protection
csrf = CSRFProtect()

# database
database = SQLAlchemy()

# A bootstrap5 class for styling client side. 
bootstrap = Bootstrap5()

# login manager
login_manager = LoginManager()

# migration
migrate = Migrate(command='db')