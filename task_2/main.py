from pymongo import MongoClient

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")  
db = client['cats_database']
collection = db['cats_collection']

# CRUD операції
def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    collection.insert_one(cat)
    print(f"Кот {name} доданий до бази даних.")

def read_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)

def read_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кот {name} не знайдений.")

def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count:
        print(f"Вік кота {name} оновлено до {new_age}.")
    else:
        print(f"Кот {name} не знайдений.")

def add_feature_to_cat(name, new_feature):
    result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
    if result.matched_count:
        print(f"Нова характеристика додана коту {name}.")
    else:
        print(f"Кот {name} не знайдений.")

def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"Кот {name} видалений з бази даних.")
    else:
        print(f"Кот {name} не знайдений.")

def delete_all_cats():
    result = collection.delete_many({})
    print(f"Видалено {result.deleted_count} котів з бази даних.")

if __name__ == "__main__":
    try:
        # Приклади використання
        create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
        
        # Читання всіх котів
        print("\nСписок всіх котів:")
        read_all_cats()
        
        # Читання кота за ім'ям
        print("\nІнформація про кота Barsik:")
        read_cat_by_name("barsik")
        
        # Оновлення віку
        update_cat_age("barsik", 4)
        
        # Додавання нової характеристики
        add_feature_to_cat("barsik", "любить спати")
        
        # Видалення кота
        delete_cat_by_name("barsik")
        
        # Видалення всіх котів
        delete_all_cats()
        
    except Exception as e:
        print(f"Сталася помилка: {e}")
