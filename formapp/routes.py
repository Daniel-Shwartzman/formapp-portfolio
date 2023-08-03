from flask import abort, render_template, request, redirect, session, url_for, flash
from flask import Blueprint
from flask_login import (
        current_user,
        login_required,
        login_user,
        logout_user
)
from formapp.extensions import database as db
from formapp.models import User, Assignment, Driving
from formapp.forms import (
    LoginForm,
    RegisterForm,
    AssignTaskForm,
    DriverForm
)
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import re
import os

formapp = Blueprint('formapp', __name__, template_folder='templates')

@formapp.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    form = RegisterForm()

    if current_user.is_authenticated:
        return redirect(url_for('formapp.index'))

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        isOfficer = form.isOfficer.data

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
        except IntegrityError:
            db.session.rollback()
            flash('Username is already taken. Please choose a different one.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Error: {}'.format(e), 'error')
    return render_template('register.html', form=form)

@formapp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('formapp.index'))
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

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

    # Clear any existing flashed messages
    session.pop('_flashes', None)

    return redirect(url_for('formapp.login'))

@formapp.route('/', strict_slashes=False, methods=['GET', 'POST'])
@formapp.route('/home', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def index():
    user = User.query.filter_by(id=current_user.id).first()
    task_form = AssignTaskForm()
    task_form.user.choices = [(user.id, user.username) for user in User.query.all() if user.id != current_user.id]

    officer_choices = [(officer.id, officer.username) for officer in User.get_officers()]
    driver_form = DriverForm()
    driver_form.commanding_officer.choices = officer_choices
    
    if driver_form.validate_on_submit():
        full_name = driver_form.full_name.data
        destination = driver_form.destination.data
        commanding_officer = driver_form.commanding_officer.data
        
        # Create a new Driving record
        Driving.create_driver(full_name, destination, commanding_officer)
        
        flash('Driver information submitted successfully.', 'success')
        return redirect(url_for('formapp.index'))
        
    if task_form.validate_on_submit():
        user_id = task_form.user.data
        task = task_form.task.data
        user.assign_task(user_id, task)
        flash('Task assigned successfully.', 'success')
        return redirect(url_for('formapp.index'))

    users = User.query.all()
    user_tasks = {user.username: [assignment.task for assignment in user.assignments] for user in users}
    
    # Fetch driving records
    drives = Driving.query.all()

    return render_template('index.html', user=user, task_form=task_form, driver_form=driver_form, users=users, user_tasks=user_tasks, drives=drives)

@formapp.route('/confirm_drive/<int:drive_id>', methods=['POST'])
@login_required
def confirm_drive(drive_id):
    if current_user.isOfficer:
        drive = Driving.query.get(drive_id)
        if drive:
            drive.isConfirmed = True
            db.session.commit()
            flash('Drive confirmed successfully.', 'success')
        else:
            flash('Drive not found.', 'danger')
    else:
        flash('You do not have permission to confirm drives.', 'danger')
    return redirect(url_for('formapp.index'))

@formapp.route('/not_confirm_drive/<int:drive_id>', methods=['POST'])
@login_required
def not_confirm_drive(drive_id):
    if current_user.isOfficer:
        drive = Driving.query.get(drive_id)
        if drive:
            drive.isConfirmed = False
            db.session.commit()
            flash('Drive status updated successfully.', 'success')
        else:
            flash('Drive not found.', 'danger')
    else:
        flash('You do not have permission to update drive status.', 'danger')
    return redirect(url_for('formapp.index'))

@formapp.route('/delete_drive/<int:drive_id>', methods=['POST'])
@login_required
def delete_drive(drive_id):
    if current_user.isOfficer:
        drive = Driving.query.get(drive_id)
        if drive:
            db.session.delete(drive)
            db.session.commit()
            flash('Drive deleted successfully.', 'success')
        else:
            flash('Drive not found.', 'danger')
    else:
        flash('You do not have permission to delete drives.', 'danger')
    return redirect(url_for('formapp.index'))
@formapp.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    if current_user.isOfficer:
        task = request.form['task']
        Assignment.delete_by_task(task)
        flash('Task deleted successfully.', 'success')
    else:
        flash('You do not have permission to delete tasks.', 'danger')
    return redirect(url_for('formapp.index'))