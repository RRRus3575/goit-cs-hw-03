import os
import psycopg2
import argparse
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

def fetch_tasks_by_user(user_id):
    query = "SELECT * FROM tasks WHERE user_id = %s"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    if tasks:
        for task in tasks:
            print(task)
    else:
        print(f"Задачи для пользователя с user_id = {user_id} не найдены")
    conn.close()

def fetch_tasks_by_status(status_name):
    query = """
    SELECT * FROM tasks 
    WHERE status_id = (SELECT id FROM status WHERE name = %s)
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (status_name,))
    tasks = cursor.fetchall()
    if tasks:
        for task in tasks:
            print(task)
    else:
        print(f"Задачи со статусом '{status_name}' не найдены")
    conn.close()

def update_task_status(task_id, new_status):
    query = """
    UPDATE tasks 
    SET status_id = (SELECT id FROM status WHERE name = %s) 
    WHERE id = %s
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (new_status, task_id))
    if cursor.rowcount > 0:
        print(f"Статус задачи с id = {task_id} успешно обновлен")
    else:
        print(f"Задача с id = {task_id} не найдена")
    conn.commit()
    conn.close()

def fetch_users_without_tasks():
    query = """
    SELECT * FROM users 
    WHERE id NOT IN (SELECT user_id FROM tasks)
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    users = cursor.fetchall()
    if users:
        for user in users:
            print(user)
    else:
        print("Пользователи без задач не найдены")
    conn.close()

def add_new_task(title, description, status_name, user_id):
    query = """
    INSERT INTO tasks (title, description, status_id, user_id) 
    VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (title, description, status_name, user_id))
    conn.commit()
    print(f"Задача '{title}' успешно добавлена для пользователя с id = {user_id}")
    conn.close()

def fetch_incomplete_tasks():
    query = """
    SELECT * FROM tasks 
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    tasks = cursor.fetchall()
    if tasks:
        for task in tasks:
            print(task)
    else:
        print("Незавершенные задачи не найдены")
    conn.close()

def delete_task(task_id):
    query = "DELETE FROM tasks WHERE id = %s"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (task_id,))
    if cursor.rowcount > 0:
        print(f"Задача с id = {task_id} успешно удалена")
    else:
        print(f"Задача с id = {task_id} не найдена")
    conn.commit()
    conn.close()

def fetch_user_by_email(email):
    query = "SELECT * FROM users WHERE email LIKE %s"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    if user:
        print(user)
    else:
        print(f"Пользователь с email {email} не найден")
    conn.close()

def update_user_fullname(user_id, new_fullname):
    query = "UPDATE users SET fullname = %s WHERE id = %s"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, (new_fullname, user_id))
    if cursor.rowcount > 0:
        print(f"Имя пользователя с id = {user_id} успешно обновлено на '{new_fullname}'")
    else:
        print(f"Пользователь с id = {user_id} не найден")
    conn.commit()
    conn.close()

def fetch_task_count_by_status():
    query = """
    SELECT s.name, COUNT(t.id) AS task_count
    FROM status s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.name
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("Данные о количестве задач по статусам не найдены")
    conn.close()

# Функция для обработки аргументов командной строки
def main():
    parser = argparse.ArgumentParser(description='Task Management Queries')
    parser.add_argument('query', type=str, help='Query to execute')
    parser.add_argument('--user_id', type=int, help='User ID for tasks')
    parser.add_argument('--status_name', type=str, help='Status name for tasks')
    parser.add_argument('--task_id', type=int, help='Task ID to update')
    parser.add_argument('--new_status', type=str, help='New status for task')
    parser.add_argument('--email', type=str, help='Email of user')
    parser.add_argument('--title', type=str, help='Title for new task')
    parser.add_argument('--description', type=str, help='Description for new task')
    parser.add_argument('--new_fullname', type=str, help='New full name for user')

    args = parser.parse_args()

    if args.query == 'fetch_tasks_by_user' and args.user_id:
        fetch_tasks_by_user(args.user_id)
    elif args.query == 'fetch_tasks_by_status' and args.status_name:
        fetch_tasks_by_status(args.status_name)
    elif args.query == 'update_task_status' and args.task_id and args.new_status:
        update_task_status(args.task_id, args.new_status)
    elif args.query == 'fetch_users_without_tasks':
        fetch_users_without_tasks()
    elif args.query == 'add_new_task' and args.title and args.description and args.status_name and args.user_id:
        add_new_task(args.title, args.description, args.status_name, args.user_id)
    elif args.query == 'fetch_incomplete_tasks':
        fetch_incomplete_tasks()
    elif args.query == 'delete_task' and args.task_id:
        delete_task(args.task_id)
    elif args.query == 'fetch_user_by_email' and args.email:
        fetch_user_by_email(args.email)
    elif args.query == 'update_user_fullname' and args.user_id and args.new_fullname:
        update_user_fullname(args.user_id, args.new_fullname)
    elif args.query == 'fetch_task_count_by_status':
        fetch_task_count_by_status()
    else:
        print("Неверные аргументы. Пожалуйста, проверьте введенные данные.")

if __name__ == "__main__":
    main()
