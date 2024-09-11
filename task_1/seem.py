import os
import psycopg2
from dotenv import load_dotenv
from faker import Faker

# Загрузка переменных из .env файла
load_dotenv()

# Инициализация Faker
fake = Faker()

# Подключение к базе данных PostgreSQL с использованием переменных окружения
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cursor = conn.cursor()

# Добавление статусов (с уникальными значениями)
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))

# Добавление пользователей (с уникальными значениями email)
for _ in range(10):
    fullname = fake.name()
    email = fake.unique.email()
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;", (fullname, email))
    print(f"Пользователь {fullname} с email {email} создан.")

print("Все пользователи успешно созданы!")

# Получение id статусов и пользователей для вставки задач
cursor.execute("SELECT id FROM status;")
status_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM users;")
user_ids = [row[0] for row in cursor.fetchall()]

# Добавление задач с рандомными значениями
for _ in range(20):  
    title = fake.sentence(nb_words=4)
    description = fake.text()
    status_id = fake.random.choice(status_ids)
    user_id = fake.random.choice(user_ids)
    cursor.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
        (title, description, status_id, user_id)
    )

conn.commit()
cursor.close()
conn.close()

print("Все задачи успешно созданы!")

