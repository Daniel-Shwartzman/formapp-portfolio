from flask import abort, render_template, request, redirect, url_for, flash
from flask import Blueprint
from flask_login import (
        current_user,
        login_required,
        login_user,
        logout_user
)
from formapp.extensions import database as db
from formapp.models import User
from formapp.forms import (
    LoginForm,
    RegisterForm
)
from datetime import datetime, timedelta
import re
import os

formapp = Blueprint('formapp', __name__, template_folder='templates')

@formapp.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('formapp.index'))
    if form.validate_on_submit():
        username = form.username.data('username')
        password = form.password.data('password')
        isOfficer = form.isOfficer.data('isOfficer')

        try:
            user = User(
                username=username,
                password=password,
                isOfficer=isOfficer
            )
            user.set_password(password)
            user.save()
            flash('You are now registered.')
            return redirect(url_for('formapp.login'))
        except Exception as e:
            flash('Error: {}'.format(e))
            return redirect(url_for('formapp.register'))
    return render_template('register.html', form=form)

@formapp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('formapp.index'))
    if form.validate_on_submit():
        username = form.username.data('username')
        password = form.password.data('password')

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User account does not exist.", 'error')
        elif not user.check_password(password):
            flash("Incorrect password.", 'error')
        else:
            login_user(user, remember=True, duration=timedelta(days=15))
            flash("You are now logged in.", 'success')
            return redirect(url_for('formapp.index'))
        return redirect(url_for('formapp.login'))
    return render_template('login.html', form=form)

@formapp.route('/logout', strict_slashes=False)
@login_required
def logout():
    logout_user()
    flash("You're logout successfully.", 'success')
    return redirect(url_for('accounts.login'))

@formapp.route('/', strict_slashes=False)
@formapp.route('/home', strict_slashes=False)
@login_required
def index():
    return render_template('index.html')



