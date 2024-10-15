from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import pymongo
from bson import ObjectId

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Debe ser la misma que en auth_service
jwt = JWTManager(app)

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["task_db"]
tasks = db["tasks"]

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user_tasks = list(tasks.find({"user": current_user}))
    for task in user_tasks:
        task['_id'] = str(task['_id'])
    return jsonify(user_tasks), 200

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    new_task = request.json
    new_task['user'] = current_user
    result = tasks.insert_one(new_task)
    return jsonify({"msg": "Task created", "id": str(result.inserted_id)}), 201

@app.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    update_data = request.json
    result = tasks.update_one(
        {"_id": ObjectId(task_id), "user": current_user},
        {"$set": update_data}
    )
    if result.modified_count:
        return jsonify({"msg": "Task updated successfully"}), 200
    return jsonify({"msg": "Task not found or you're not authorized"}), 404

@app.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    result = tasks.delete_one({"_id": ObjectId(task_id), "user": current_user})
    if result.deleted_count:
        return jsonify({"msg": "Task deleted successfully"}), 200
    return jsonify({"msg": "Task not found or you're not authorized"}), 404

if __name__ == '__main__':
    app.run(port=5001)
