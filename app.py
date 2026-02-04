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
    new_task = Task(id=task_control_id, title=request.get_json().get("title"), description=request.get_json().get("description", ""))
    task_list.append(new_task)
    task_control_id += 1
    print(task_list)
    return jsonify({"message": "Task added successfully"})

@app.route("/task", methods=["GET"])
def get_tasks():
    task_list_dict = [task.to_dict() for task in task_list]
    
    output = {
        "tasks": task_list_dict,
        "total_tasks": len(task_list_dict)
    }
    
    return jsonify(output)

@app.route("/task/<int:idOneTask>", methods=["GET"])
def getOneTask(idOneTask):
    global task_list    
    for t in task_list:
        if t.id == idOneTask:
            return jsonify(t.to_dict())
    return jsonify({"message": "Task not found with ID selected"}), 404

@app.route("/task/<int:idPutTask>", methods=["PUT"])
def getPutTask(idPutTask):
    global task_list
    taskPut = None
    for t in task_list:
        if t.id == idPutTask:
            taskPut = t
    if not taskPut:
        return jsonify({"Message": "Task not found with ID selected"}), 404
    taskPut.title = request.get_json().get("title")
    taskPut.description = request.get_json().get("description")
    taskPut.completed = request.get_json().get("completed")
    
    return jsonify({"Message": "Task updated successfully"})
    
if __name__ == "__main__":
    app.run(debug=True)
    