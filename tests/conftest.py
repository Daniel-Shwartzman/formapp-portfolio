import pytest
from formapp import create_app
from formapp.extensions import csrf
from formapp.models import User
from formapp.forms import RegisterForm

@pytest.fixture
def app():
    _app = create_app(testing=True)
    with _app.app_context():
        csrf.init_app(_app)
        yield _app

@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client

@pytest.fixture
def registered_user(client):
    form = RegisterForm()
    form.username.data = 'testuser'
    form.password.data = 'testpassword'
    form.isOfficer.data = True
    form.submit.data = True

    assert form.validate()

    response = client.post('/register', data=form.data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    return user

@pytest.fixture
def officer_user(client):
    form = RegisterForm()
    form.username.data = 'officer'
    form.password.data = 'officerpassword'
    form.isOfficer.data = True
    form.submit.data = True

    assert form.validate()

    response = client.post('/register', data=form.data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

    user = User.query.filter_by(username='officer').first()
    assert user is not None
    return user
