from db_connect import db


# Connect to MongoDB
db = db
db_list = db['todo_list']
db_register = db['todo_register']
db_status =  db['todo_status']

