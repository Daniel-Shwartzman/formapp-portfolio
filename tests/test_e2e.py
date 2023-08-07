import pytest
import requests

# Replace with the URL where your Flask app is running
BASE_URL = "http://localhost:5000"

@pytest.fixture
def cookies():
    url = f"{BASE_URL}/login"
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    return response.cookies

def test_register():
    url = f"{BASE_URL}/register"
    data = {
        "username": "testuser",
        "password": "testpassword",
        "isOfficer": False
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200

def test_logout(cookies):
    url = f"{BASE_URL}/logout"
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200

def test_index(cookies):
    url = f"{BASE_URL}/"
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    # Add additional assertions as needed based on your route's response content

# Run the tests
if __name__ == "__main__":
    pytest.main(["-v", "test_e2e.py"])
