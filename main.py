from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

from flask import render_template

@app.route("/")
def translate_form():
    return render_template("home.html")


CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        task_content = request.json.get("task")
        if task_content:
            new_task = Task(description=task_content)
            db.session.add(new_task)
            db.session.commit()
        return jsonify({"message": "Task added successfully"}), 201
    tasks = Task.query.all()
    tasks_list = [{"id": task.id, "description": task.description, "completed": task.completed} for task in tasks]
    return jsonify(tasks_list)

@app.route("/tasks/<int:task_id>", methods=["PUT", "DELETE"])
def modify_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    if request.method == "PUT":
        task_content = request.json.get("task")
        if task_content:
            task.description = task_content
            db.session.commit()
            return jsonify({"message": "Task updated successfully"})
    if request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})

@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    task.completed = True
    db.session.commit()
    return jsonify({"message": "Task marked as complete"})

@app.route("/tasks/<int:task_id>/incomplete", methods=["PUT"])
def mark_as_incomplete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    task.completed = False
    db.session.commit()
    return jsonify({"message": "Task marked as incomplete"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)