from src.app import app
import pytest
from pprint import pprint

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    
def testPostTaskStatus(client):
    test_new_task = {
        "title": "To study Python"
    }
    response = client.post('/task', json=test_new_task)

    assert response.status_code == 200 or 201
    
def testGetTasksStatus(client):
    response = client.get('/task')  
    test_get_task = response.get_json()
    
    print("\n" + "="*100)
    print("LOG: ")
    pprint(test_get_task['tasks'])
    print("\n" + "="*100)
    
    list_words = ["id", "title", "description", "completed"]
    for i in list_words:
        name_replace = any(i in t for t in test_get_task['tasks'])
        assert True == name_replace
        
def testPutTask(client):
    test_put_json = {
        "completed": True
    }
    
    response = client.put('/task/1', json=test_put_json)
    
    assert response.status_code == 200    
    
def testGetOneTaskStatus(client):
    response = client.get('/task/1')
    test_task_list = response.get_json()
    print("\n" + "="*100)
    print("LOG:")
    pprint(test_task_list)
    print("="*100)
    
    list_words = ["id", "title", "description", "completed"]    
    assert response.status_code == 200
    assert "id" in test_task_list
    assert "title" in test_task_list
    assert "description" in test_task_list
    assert "completed" in test_task_list
    
