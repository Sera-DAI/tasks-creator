from src.app import app
import pytest
from pprint import pprint

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    
def testPostTaskStatus(client):
    list_words = ['Python', 'Java', 'Go', 'C', 'C#', 'C+']
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
    response = client.get('/task')  
    test_get_task = response.get_json()
    
    print("\n" + "="*100)
    print("LOG GET ALL TASKS:")
    pprint(test_get_task)
    
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
    print("LOG GET ONE TASK:")
    pprint(test_task_list)
    print("="*100)
    
    list_words = ["id", "title", "description", "completed"]    
    for i in list_words:
        name_replace = any(i in t for t in test_task_list)
        assert True == name_replace
        
def testDeletetask(client):
    requests = {
        "id_1": client.get('/task/1'),
        "id_2": client.delete('/task/1'),
        "id_3": client.get('/task/1')
    }
    dict_test = {
        "requisitions": requests,
        "responses": {key: value.get_json() for key, value in requests.items()}
        }
    
    print("\n" + "="*100)
    print("LOG GET BEFORE DELETE:")
    pprint(dict_test["responses"]["id_1"])
    print("LOG DELETE:")
    pprint(dict_test["responses"]["id_2"])
    print("LOG GET AFTER DELETE:")
    pprint(dict_test["responses"]["id_3"])
    print("="*100)
    

    for keys in dict_test["requisitions"]:
        assert (status := dict_test["requisitions"][keys].status_code) in [200, 201]
    assert "Message" in (status_delete := dict_test["responses"]["id_2"]) 
    assert (status_delete := dict_test["responses"]["id_2"]["Message"]) == "Task deleted successfully"
    