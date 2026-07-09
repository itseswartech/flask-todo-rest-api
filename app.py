from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Flask To-Do REST API is Running!"

# CREATE TASK
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    title = data['title']
    description = data.get('description', '')

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(title, description) VALUES(?, ?)",
        (title, description)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task Created Successfully"
    }), 201

# GET ALL TASKS
@app.route('/tasks', methods=['GET'])
def get_tasks():

    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return jsonify([dict(task) for task in tasks])

# UPDATE TASK
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):

    data = request.get_json()

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title=?, description=?, completed=?
        WHERE id=?
    """,
    (
        data['title'],
        data['description'],
        data['completed'],
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task Updated Successfully"
    })
# DELETE TASK
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task Deleted Successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)