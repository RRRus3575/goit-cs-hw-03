from pymongo import MongoClient

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")  
db = client['cats_database'] 
collection = db['cats_collection']  

