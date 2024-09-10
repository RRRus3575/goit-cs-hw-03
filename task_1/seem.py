from faker import Faker
import psycopg2

fake = Faker()

# Параметры подключения к базе данных
conn = psycopg2.connect(dbname='task_management', user='postgres', password='your_new_password', host='localhost')
cursor = conn.cursor()

# Добавление статусов
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))

# Добавление пользователей
for _ in range(10):  
    fullname = fake.name()
    email = fake.unique.email()
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;", (fullname, email))

# Получение id статусов и пользователей
cursor.execute("SELECT id FROM status;")
status_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM users;")
user_ids = [row[0] for row in cursor.fetchall()]

# Добавление задач
for _ in range(20):  # Количество задач
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

