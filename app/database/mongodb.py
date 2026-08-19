from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

mongo_db = client["task_manager"]

historial_collection = mongo_db["historial_tareas"]