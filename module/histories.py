from os import get_terminal_size, name
from .dbdriver import db

class histories():
    def __init__(self, booking_id,gmail_user,time,location,destination,status):
        self.booking_id = booking_id
        self.gmail_user = gmail_user
        self.time = time
        self.location = location
        self.destination = destination
        self.status = status
        pass
    
    def add_history(self):
        data = {
            "booking_id": self.booking_id,
            "gmail_user": self.gmail_user,
            "time": self.time,
            "location": self.location,
            "destination": self.destination,
            "status": self.status
        }
        db.histories.insert_one({"histories": data})
  
