from django.db import models
from .db_connect import databse
# Create your models here.

db_list = databse.todo_list
db_register  = databse.todo_register
db_status = databse.todo_status