from pymongo import MongoClient

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Або використовуйте Atlas URL
db = client['cats_database']  # Створює базу даних cats_database
collection = db['cats_collection']  # Створює колекцію cats_collection

