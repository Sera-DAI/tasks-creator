from flask import Flask, request, jsonify
from src.task_create import Task

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

@app.route("/task/<int:id_one_taskk>", methods=["GET"])
def getOneTask(id_one_taskk):
    global task_list    
    idx_task_verify = next((t.to_dict() for t in task_list if t.id == id_one_taskk), None)
    return jsonify(idx_task_verify)
    return jsonify({"message": "Task not found with ID selected"}), 404

@app.route("/task/<int:idPutTask>", methods=["PUT"])
def getPutTask(idPutTask):
    global task_list
    task_put = next((t for t in task_list if t.id == idPutTask), None)
    if not task_put:
        return jsonify({"Message": "Task not found with ID selected"}), 404
    task_put.title = request.get_json().get("title")
    task_put.description = request.get_json().get("description")
    task_put.completed = request.get_json().get("completed")
    
    return jsonify({"Message": "Task updated successfully"})
    
@app.route("/task/<int:id_delete_task>", methods=["DELETE"])
def deleteTask(id_delete_task):
    global task_list
    idx_task_verify = next((i for i, t in enumerate(task_list) if t.id == id_delete_task), None)
    if not idx_task_verify:
        return jsonify({"Message": "Task not found with ID selected"}), 404
    task_list.pop(idx_task_verify)
    return jsonify({"Message": "Task deleted successfuly"})

if __name__ == "__main__":
    app.run(debug=True)
    