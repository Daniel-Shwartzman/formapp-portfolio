from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash
)
from flask import Blueprint
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from sqlalchemy.exc import IntegrityError  # Third-party import
from datetime import timedelta  # Standard library import

from formapp.extensions import database as db
from formapp.models import (
    User,
    Assignment,
    Driving,
    Flying
)
from formapp.forms import (
    LoginForm,
    RegisterForm,
    AssignTaskForm,
    FlyingForm,
    DriverForm,
    PasswordForm
)

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
            error_message = f"An error occurred: {e}"
            flash(error_message, 'error')
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
    flying_form = FlyingForm()
    task_form.user.choices = [(user.id, user.username) for user in User.query.all() if user.id != current_user.id]

    officer_choices = [(officer.id, officer.username) for officer in User.get_officers()]
    driver_form = DriverForm()
    driver_form.commanding_officer.choices = officer_choices
    if flying_form.validate_on_submit():
        full_name = flying_form.full_name.data
        start_date = flying_form.start_date.data
        end_date = flying_form.end_date.data
        location = flying_form.location.data

        # Create a new Flying record
        Flying.create_flying(full_name, start_date, end_date, location)

        flash('Flying information submitted successfully.', 'success')
        return redirect(url_for('formapp.index'))
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
    # Fetch flying records
    flying_entries = Flying.query.all()
    # Fetch driving records
    drives = Driving.query.all()
    return render_template('index.html', user=user, task_form=task_form,
                        driver_form=driver_form, users=users,
                        user_tasks=user_tasks, drives=drives,
                        flying_form=flying_form,
                        flying_entries=flying_entries)
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

@formapp.route('/confirm_flying/<int:flying_id>', methods=['POST'])
@login_required
def confirm_flying(flying_id):
    if current_user.isOfficer:
        fly = Flying.query.get(flying_id)
        if fly:
            fly.isConfirmed = True
            db.session.commit()
            flash('Flying record confirmed successfully.', 'success')
        else:
            flash('Flying record not found.', 'danger')
    else:
        flash('You do not have permission to confirm flying records.', 'danger')
    return redirect(url_for('formapp.index'))

@formapp.route('/not_confirm_flying/<int:flying_id>', methods=['POST'])
@login_required
def not_confirm_flying(flying_id):
    if current_user.isOfficer:
        fly = Flying.query.get(flying_id)
        if fly:
            fly.isConfirmed = False
            db.session.commit()
            flash('Flying record status updated successfully.', 'success')
        else:
            flash('Flying record not found.', 'danger')
    else:
        flash('You do not have permission to update flying record status.', 'danger')
    return redirect(url_for('formapp.index'))

@formapp.route('/delete_flying/<int:flying_id>', methods=['POST'])
@login_required
def delete_flying(flying_id):
    # delete the specific flying record
    if current_user.isOfficer:
        fly = Flying.query.get(flying_id)
        if fly:
            db.session.delete(fly)
            db.session.commit()
            flash('Flying record deleted successfully.', 'success')
        else:
            flash('Flying record not found.', 'danger')
    else:
        flash('You do not have permission to delete flying records.', 'danger')
    return redirect(url_for('formapp.index'))

@formapp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = PasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password updated successfully.', 'success')
            return redirect(url_for('formapp.index'))

        flash('Old password is incorrect.', 'danger')

    return render_template('settings.html', form=form)
