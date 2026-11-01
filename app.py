import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tasks.db"

app = Flask(__name__)


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    with get_db() as db:
        tasks = db.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    return jsonify([dict(task) for task in tasks])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title:
        return jsonify({"error": "Введите название задачи"}), 400

    if len(title) > 150 or len(description) > 1000:
        return jsonify({"error": "Слишком длинный текст"}), 400

    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title, description)
        )
        task = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

    return jsonify(dict(task)), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    if "completed" not in data or not isinstance(
        data["completed"], bool
    ):
        return jsonify({"error": "Некорректный статус"}), 400

    with get_db() as db:
        cursor = db.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (int(data["completed"]), task_id)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Задача не найдена"}), 404

        task = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

    return jsonify(dict(task))


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )

    if cursor.rowcount == 0:
        return jsonify({"error": "Задача не найдена"}), 404

    return jsonify({"message": "Задача удалена"})


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
