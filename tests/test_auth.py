import pytest
from formapp import create_app, db
from formapp.models import User
from formapp.forms import RegisterForm, LoginForm

def test_register_route(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_login_route(client, registered_user):  # Pass the registered_user fixture
    response = client.get('/login')
    assert response.status_code == 200

    # Create a LoginForm instance and fill in the data
    form = LoginForm()
    form.username.data = 'testuser'
    form.password.data = 'testpassword'
    form.remember.data = True
    form.submit.data = True  # Add this line to simulate form submission

    # Check if the form data matches the form definition
    assert form.validate()

    # Test submitting a valid login form
    response = client.post('/login', data=form.data, follow_redirects=True)
    assert response.status_code == 200
    assert b'IDF - Forms' in response.data
