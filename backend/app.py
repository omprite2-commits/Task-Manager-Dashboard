import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, completed BOOLEAN)''')
    conn.commit()
    conn.close()

init_db()

# 1. GET: Fetch all tasks from the database
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    tasks = [{"id": r[0], "title": r[1], "completed": bool(r[2])} for r in rows]
    conn.close()
    return jsonify(tasks)

# 2. POST: Add a new task to the database
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (data['title'], False))
    conn.commit()
    task_id = c.lastrowid
    conn.close()
    return jsonify({"id": task_id, "title": data['title'], "completed": False}), 201

# 3. DELETE: Remove a task from the database
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted successfully"}), 200

# 4. PUT: Update task status (Completed/Pending)
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed=? WHERE id=?", (data['completed'], task_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)