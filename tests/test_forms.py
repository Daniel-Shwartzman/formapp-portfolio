from formapp.models import Flying, Driving, Assignment
from formapp.forms import FlyingForm, DriverForm, AssignTaskForm


def test_submit_flying_form(client):
    # Login as the registered user
    login_response = client.post(
        '/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    assert login_response.status_code == 200

    # Create a FlyingForm instance and fill in the data
    form = FlyingForm()
    form.full_name.data = 'John Doe'
    form.start_date.data = '2023-08-15'
    form.end_date.data = '2023-08-20'
    form.location.data = 'Some Location'
    form.submit.data = True  # Simulate form submission

    # Submit the flying form
    form_response = client.post('/home', data=form.data, follow_redirects=True)
    assert form_response.status_code == 200
    assert b'Flying information submitted successfully.' in form_response.data

    # Verify the data in the database
    submitted_flying = Flying.query.filter_by(full_name='John Doe').first()
    assert submitted_flying is not None
    assert submitted_flying.start_date == '2023-08-15'
    assert submitted_flying.end_date == '2023-08-20'
    assert submitted_flying.location == 'Some Location'
    #Check updates
    form_response = client.post('/home#tab5', follow_redirects=True)
    assert form_response.status_code == 200
    assert b'John Doe' in form_response.data

def test_submit_driver_form(client, officer_user):
    # Login as the registered user
    login_response = client.post(
        '/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    assert login_response.status_code == 200

    # Create a DriverForm instance and fill in the data
    form = DriverForm()
    form.full_name.data = 'Jane Smith'
    form.destination.data = 'Another Location'
    form.commanding_officer.data = officer_user.id  # Assign the officer user's ID
    form.submit.data = True  # Simulate form submission

    # Submit the driver form
    form_response = client.post('/home', data=form.data, follow_redirects=True)
    assert form_response.status_code == 200
    assert b'Driver information submitted successfully' in form_response.data

    # Verify the data in the database
    submitted_driver = Driving.query.filter_by(full_name='Jane Smith').first()
    assert submitted_driver is not None
    assert submitted_driver.destination == 'Another Location'

    #Check updates
    form_response = client.post('/home#tab5', follow_redirects=True)
    assert form_response.status_code == 200
    assert b'Jane Smith' in form_response.data

def test_assignments(client, registered_user):
    login_response = client.post(
    '/login', data={'username': 'officer', 'password': 'officerpassword'}, follow_redirects=True)
    assert login_response.status_code == 200 
    form =  AssignTaskForm()
    form.user.data = registered_user.id
    form.task.data = 'Test Task'
    form.submit.data = True

    form_response = client.post('/home', data=form.data, follow_redirects=True)
    assert form_response.status_code == 200
    assert b'Task assigned successfully.' in form_response.data

    submitted_task = Assignment.query.filter_by(task='Test Task').first()
    assert submitted_task is not None

    #Check updates
    form_response = client.post('/home#tab5', follow_redirects=True)
    assert form_response.status_code == 200
    assert b'Test Task' in form_response.data
