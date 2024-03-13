from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['todo']

# Define your database objects

db.uid.create_index([("logintime", 1)], expireAfterSeconds=300)

