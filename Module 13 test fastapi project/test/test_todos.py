from test.test_main import client
from main import app
from fastapi import status
from router.auth import get_current_user

def override_get_current_user():
    return {
        'id' : 1,
        'username' : 'testuser'
    }

app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_todos():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK