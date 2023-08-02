import os
from flask import Flask
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'formapp', 'static', 'images')

load_dotenv(os.path.join(BASE_DIR, '.env'))

def create_app():
    app = Flask(__name__, template_folder='templates')

    # application configuration.
    config_application(app)
    # config application extension. 
    config_extensions(app)
    # register account blueprint.
    config_blueprint(app)

    return app

def config_application(app):
    # Application configuration
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = os.urandom(12)
    
    # SQLAlchemy configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db' # later change to mysql
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

def config_blueprint(app):
    from routes import formapp
    app.register_blueprint(formapp)

def config_extensions(app):
    from extensions import database
    from extensions import migrate
    from extensions import login_manager
    from extensions import csrf

    database.init_app(app)
    migrate.init_app(app, db=database)
    login_manager.init_app(app)
    csrf.init_app(app)

def config_manager(manager):
    from models import User

    manager.login_message = "You are not logged in to your account."
    manager.login_message_category = "warning"
    manager.login_view = "accounts.login"

    @manager.user_loader
    def user_loader(id):
        return User.query.get_or_404(id)

def config_errorhandler(app): #update according to your needs
    """
    Configure error handlers for application.
    """
    from flask import render_template
    from flask import redirect
    from flask import url_for
    from flask import flash

    @app.errorhandler(400)
    def bad_request(e):
        flash("Something went wrong.", 'error')
        return redirect(url_for('accounts.index'))
    
    @app.errorhandler(401)
    def unauthorized(e):
        flash("You are not authorized to perform this action.", 'error')
        return redirect(url_for('accounts.index'))
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        flash("Method not allowed.", 'error')
        return redirect(url_for('accounts.index'))

    @app.errorhandler(500)
    def database_error(e):
        flash("Internal server error.", 'error')
        return redirect(url_for('accounts.index'))