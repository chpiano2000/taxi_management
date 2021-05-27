from os import get_terminal_size, name
from .dbdriver import db

class user():
    def __init__(self, name, gmail, sex, password, histories):
        self.name = name
        self.gmail = gmail
        self.sex = sex
        self.password = password
        self.histories = histories
        pass
    
    def add_usr(self):
        data = {
            "name": self.name,
            "sex": self.sex,
            "gmail": self.gmail,
            "password": self.password
        }
        db.users.insert_one(data)

    def update_usr_name(self):
        db.users.update_one({'gmail': self.gmail}, self.get_name_data())

    def get_name_data(self):
        data = {"$set": {"name": self.name}}
        return data

    def getHistory(self):
        cursor = db.histories.find({"gmail": gmail})
        return list(cursor)

