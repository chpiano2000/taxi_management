from os import get_terminal_size, name
from .dbdriver import db

class driver():
    def __init__(self, name,sex,car,gmail,password):
        self.name = name
        self.gmail = gmail
        self.sex = sex
        self.password = password
        self.car = car
        pass

    def find_driver(self):
        return list(db.drivers.find({"gmail": self.gmail}))

    def add_driver(self):
        data = {
            "name": self.name,
            "sex": self.sex,
            "car": self.car,
            "gmail": self.gmail,
            "password": self.password,
        }
        db.drivers.insert_one(data)
    
    def update_usr_name(self):
        db.users.update_one({'gmail': self.gmail}, self.get_name_data())

    def get_name_data(self):
        data = {"$set": {"name": self.name}}
        return data

    
