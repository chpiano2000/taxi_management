from os import get_terminal_size, name


class user():
    name = ''
    gmail = ''
    sex=''
    password=''
    histories = ''
    def __init__(self, name, gmail, sex, password, histories):
        self.name = name
        self.gmail = gmail
        self.sex = sex
        self.password = password
        self.histories = histories
        
        pass
    
    def get_age(self):
        return self._age

    def get_name_data(self):
        data = {"$set": {"name": self.name}}
        return data
      
    def get_data_add_usr(self):
        data = {
            "name": self.name,
            "sex": self.sex,
            "gmail": self.gmail,
            "password": self.password
        }
        return data

    # setter method
    def set_age(self, x):
        self._age = x
  
