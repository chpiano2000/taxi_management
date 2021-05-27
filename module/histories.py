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
            "status": "false"
        }
        db.histories.insert_one({"histories": data})
  
    def get_booking(self):
        cursor = db.histories.find({"histories.booking_id": f"{self.booking_id}"})
        return list(cursor)

    def update_booking(self):
        db.histories.update_one({"histories.booking_id": f"{self.booking_id}"}, {"$set": {"histories.status": "true", "driver": self.gmail_user}})