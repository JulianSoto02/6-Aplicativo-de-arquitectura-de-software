from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_SERVICE = "http://localhost:5000"
TASK_SERVICE = "http://localhost:5001"
NOTIFICATION_SERVICE = "http://localhost:5002"

@app.route('/register', methods=['POST'])
def register():
    return requests.post(f"{AUTH_SERVICE}/register", json=request.json).content

@app.route('/login', methods=['POST'])
def login():
    return requests.post(f"{AUTH_SERVICE}/login", json=request.json).content

@app.route('/tasks', methods=['GET'])
def get_tasks():
    token = request.headers.get('Authorization')
    return requests.get(f"{TASK_SERVICE}/tasks", headers={'Authorization': token}).content

@app.route('/tasks', methods=['POST'])
def create_task():
    token = request.headers.get('Authorization')
    response = requests.post(f"{TASK_SERVICE}/tasks", headers={'Authorization': token}, json=request.json)
    if response.status_code == 201:
        notification = {"type": "task_created", "user": request.json.get('user'), "task": request.json.get('title')}
        requests.post(f"{NOTIFICATION_SERVICE}/notify", json=notification)
    return response.content

@app.route('/tasks/<task_id>', methods=['PUT', 'DELETE'])
def manage_task(task_id):
    token = request.headers.get('Authorization')
    if request.method == 'PUT':
        return requests.put(f"{TASK_SERVICE}/tasks/{task_id}", headers={'Authorization': token}, json=request.json).content
    elif request.method == 'DELETE':
        return requests.delete(f"{TASK_SERVICE}/tasks/{task_id}", headers={'Authorization': token}).content

if __name__ == '__main__':
    app.run(port=5003)
