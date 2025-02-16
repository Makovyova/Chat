import sqlite3
import json

DATABASE_NAME = 'english_bot.db'

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            level INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            question TEXT,
            options TEXT,  -- this will hold options as JSON string
            answer TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_user(user_id, user_name):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name))
    conn.commit()
    conn.close()

def user_exists(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)

def add_task(task_type, question, options, answer):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    options_json = json.dumps(options)
    cursor.execute("INSERT INTO tasks (type, question, options, answer) VALUES (?, ?, ?, ?)", (task_type, question, options_json, answer))
    conn.commit()
    conn.close()

def get_tasks(task_type):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, question, options, answer FROM tasks WHERE type = ?", (task_type,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_user_data(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, level FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def save_progress(user_id, task_id, correct):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Проверяем, есть ли уже запись для данного пользователя и задания
    cursor.execute("SELECT * FROM user_progress WHERE user_id = ? AND task_id = ?", (user_id, task_id))
    existing_record = cursor.fetchone()
    
    if existing_record:
        # Обновляем существующую запись
        cursor.execute("UPDATE user_progress SET correct = ? WHERE user_id = ? AND task_id = ?", (correct, user_id, task_id))
    else:
        # Создаем новую запись
        cursor.execute("INSERT INTO user_progress (user_id, task_id, correct) VALUES (?, ?, ?)", (user_id, task_id, correct))
        
    conn.commit()
    conn.close()

def update_user_level(user_id, new_level):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET level = ? WHERE user_id = ?", (new_level, user_id))
    conn.commit()
    conn.close()

def get_user_progress(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.question, up.correct
        FROM user_progress AS up
        JOIN tasks AS t ON up.task_id = t.task_id
        WHERE up.user_id = ?
    """, (user_id,))
    progress = cursor.fetchall()
    conn.close()
    return progress
