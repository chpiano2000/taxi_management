from os import get_terminal_size, name
from .dbdriver import db

class admin():
    def __init__(self, name,password):
        self.name = name
        self.password = password
        pass

    def check_auth(self):
        cursor = db.admin.find({"name": self.name, "password": self.password}, {"_id": 0})
        return list(cursor)

    def change_name(self, new_name):
        db.admin.update({"name": self.name}, {"$set": {"name": new_name}})
    
   