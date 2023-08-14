import pytest
from formapp import create_app, db
from formapp.models import User
from formapp.forms import RegisterForm, LoginForm

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        from formapp.extensions import csrf
        csrf.init_app(app)
        yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:  # Use the test client context
        yield client

@pytest.fixture
def registered_user(client):
    # Create a RegisterForm instance and fill in the data
    form = RegisterForm()
    form.username.data = 'testuser'
    form.password.data = 'testpassword'
    form.isOfficer.data = True
    form.submit.data = True  # Add this line to simulate form submission

    # Check if the form data matches the form definition
    assert form.validate()

    # Register the user
    response = client.post('/register', data=form.data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

    # Get the registered user from the database
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    return user

@pytest.fixture
def officer_user(client):
    # Create a RegisterForm instance and fill in the data
    form = RegisterForm()
    form.username.data = 'officer'
    form.password.data = 'officerpassword'
    form.isOfficer.data = True
    form.submit.data = True  # Add this line to simulate form submission

    # Check if the form data matches the form definition
    assert form.validate()

    # Register the officer user
    response = client.post('/register', data=form.data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

    # Get the registered officer user from the database
    user = User.query.filter_by(username='officer').first()
    assert user is not None
    return user
