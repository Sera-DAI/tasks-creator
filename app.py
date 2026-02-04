from flask import Flask, request, jsonify
from modules.task_create import Task

app = Flask(__name__)

task_list = []
task_control_id = 1

@app.route("/")
def about():
    return "This is about API test"

@app.route("/task", methods=["POST"])
def add_task():
    global task_control_id
    data = request.get_json()   
    new_task = Task(id=task_control_id, title=data.get("title"), description=data.get("description", ""))
    task_list.append(new_task)
    task_control_id += 1
    print(task_list)
    return jsonify({"message": "Task added successfully"})

@app.route("/task", methods=["GET"])
def get_task():
    task_list_dict = [task.to_dict() for task in task_list]
    
    output = {
        "tasks": task_list_dict,
        "total_tasks": 0
    }
    
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
    