from src.app import app
import pytest
from pprint import pprint

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    
list_words = ['Python', 'Java', 'Go', 'C', 'C#', 'C+']
def testPostTaskStatus(client):
    print("\n" + "="*100)
    print("LOG POST TASKS:")
    for word in list_words:
        test_new_task = {
            "title": f"To study {word}",
            "description": f"test + {word}"
        }
        response = client.post('/task', json=test_new_task)
        print()
    assert response.status_code == 200
    
def testGetTasksStatus(client):
    for i in list_words:
        response = client.get(f'/task')  
    
    response_get_test = response.get_json()
    print("\n" + "="*100)
    print("LOG GET ALL TASKS:")
    pprint(response_get_test)
    
    list_variables = ["id", "title", "description", "completed"]
    for i in list_variables:
        name_replace = any(i in t for t in response_get_test['tasks'])
        assert True == name_replace
        
    
def testGetOneTaskStatus(client):
    test_task_list = []
    for idx, t in enumerate(list_words):
        response = client.get(f'/task/{idx+1}')
        test_task_list.append(response.get_json())
        
    print("\n" + "="*100)
    print("LOG GET ONE TASK:")
    pprint(test_task_list)
    print("="*100)
    
    list_variables = ["id", "title", "description", "completed"]    
    for dct in test_task_list:
            for i in list_variables:
                assert i in dct, f"The field {i} don't being presente in {dct}"   
        
def testPutTask(client):
    test_put_json = {
        "completed": True
    }
    
    id_url = 1
    for t in list_words:
        response = client.put(f'/task/{id_url}', json=test_put_json)           
    get_response = client.get('/task')
        
    print("\n" + "="*100)
    print("LOG AFTER PUT")
    pprint(get_response.get_json())
    
    assert response.status_code == 200

def testDeletetask(client):
    list_delete = []
    for idx, l in enumerate(list_words):
        response = client.delete(f'/task/{idx+1}')
        list_delete.append(response.get_json())
    get_response = client.get('/task')
    
    print("\n" + "="*100)
    print("LOG DELETE:")
    pprint(list_delete)
    print("\n" + "="*100)
    pprint(get_response.get_json())
    
    assert response.status_code in [200, 201]
    for idx, l in enumerate(list_words):
        assert "Message" in list_delete[idx]
        assert "Task deleted successfully" in list_delete[idx]["Message"]