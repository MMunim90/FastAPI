from test.test_main import client
from main import app
from fastapi import status
from router.auth import get_current_user
from database import SessionLocal
from models import Todos

def override_get_current_user():
    return {
        'id' : 1,
        'username' : 'testuser'
    }
    
    
def test_todo():
    db = SessionLocal()
    
    # remove old test data if its exists
    db.query(Todos).filter(Todos.id == 1011).delete()
    
    todo = Todos(
        id = 1011,
        title = 'Testing',
        description = 'Testing',
        priority = 5,
        completed = True,
        owner_id = 1
    )
    
    db.add(todo)
    db.commit()

app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_todos():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    
    
def test_read_specific_todos():
    response = client.get('/todo/1011')
    assert response.status_code == status.HTTP_200_OK
    
    
def test_create_todo():
    db = SessionLocal()
    db.query(Todos).filter(Todos.id == 0).delete()
    db.commit()
    
    request_data = {
        "id": 0,
        "title": "string",
        "description": "string",
        "priority": 1,
        "completed": False
    }
    response = client.post('/create-todo', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'message' : 'Todo created successfully'}
    
    
    
def test_update_todo():
    request_data = {
        "title": "Testing updated",
    }
    response = client.put('/update_todo/1011', json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message' : 'Todo updated successfully'}
    
    
    
def test_delete_todo():
    response = client.delete('/delete_todo/1011')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message' : 'Todo deleted successfully'}