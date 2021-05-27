import pymongo
from decouple import config
# from module.user import user

url = config('URL')
mongo = pymongo.MongoClient(url)
db = mongo.taxi_management

######################## USER #####################################

def add_users(name,sex,gmail,password):

    
    data = {
            "name": name,
            "sex": sex,
            "gmail": gmail,
            "password": password
        }
    db.users.insert_one(data)

def check_user(gmail):
    return list(db.users.find({"gmail": gmail}))

def update_name(password, name, gmail):
    db.users.update_one({'password': password}, {"$set": {"name": name, "gmail": gmail}})

def check_history(gmail):
    cursor = db.histories.find({"gmail": gmail})
    return list(cursor)

def insert_histories(data):
    db.histories.insert_one({"histories": data})

def update_histories(gmail, data):
    db.histories.update_one({"gmail": gmail}, {"$push": {'histories': data}})

def query_histories():
    pipeline = [
        {
            '$unwind': {
                'path': '$histories'
            }
        }, {
            '$project': {
                'histories': 1,
                "_id": 0
            }
        }
    ]

    data = list(db.histories.aggregate(pipeline))
    return data

def update_driver_rating(driver, rating, star):
    db.drivers.update_one({"name": driver}, {"$push": {"star": {"star": star, "rating": rating}}})

def check_status(booking_id):
    pipeline = [
        {
            '$match': {
                'histories.booking_id': booking_id
            }
        }, {
            '$project': {
                'status': '$histories.status'
            }
        }
    ]
    return list(db.histories.aggregate(pipeline))

######################## Driver #####################################

def check_driver(gmail):
    return list(db.drivers.find({"gmail": gmail}))

def add_driver(data):
    db.drivers.insert_one(data)

def show_history_driver():
    pipeline = [
        {
            '$sort': {
                '_id': -1
            }
        }, {
            '$limit': 3
        }
    ]
    return list(db.histories.aggregate(pipeline))

def check_id(booking_id):
    cursor = db.histories.find({"histories.booking_id": f"{booking_id}"})
    return list(cursor)

def update_status(booking_id, gmail):
    db.histories.update_one({"histories.booking_id": f"{booking_id}"}, {"$set": {"histories.status": "true", "driver": gmail}})

######################## Admin #####################################

def check_admin(name, password):
    cursor = db.admin.find({"name": name, "password": password}, {"_id": 0})
    return list(cursor)

def query_by_user():
    pipeline = [
        {
            '$lookup': {
                'from': 'drivers', 
                'localField': 'gmail_driver', 
                'foreignField': 'gmail', 
                'as': 'drivers'
            }
        }, {
            '$unwind': {
                'path': '$drivers'
            }
        }, {
            '$project': {
                '_id': 0,
                'booking_id': '$histories.booking_id', 
                'gmail_user': '$histories.gmail_user', 
                'time': '$histories.time', 
                'location': '$location', 
                'destination': '$histories.destination', 
                'driver_name': '$drivers.name', 
                'driver_car': '$drivers.car'
            }
        }
    ]
    cursor = db.histories.aggregate(pipeline)
    return list(cursor)

def query_by_driver():
    pipeline = [
        {
            '$lookup': {
                'from': 'users', 
                'localField': 'histories.gmail_user', 
                'foreignField': 'gmail', 
                'as': 'users'
            }
        }, {
            '$unwind': {
                'path': '$users'
            }
        }, {
            '$project': {
                '_id': 0, 
                'booking_id': '$histories.booking_id', 
                'gmail_user': '$histories.gmail_user', 
                'time': '$histories.time', 
                'location': '$location', 
                'destination': '$histories.destination', 
                'driver_name': '$users.name', 
                'driver_car': '$userss.car', 
                'gmail_driver': '$gmail_driver'
            }
        }
    ]

    cursor = db.histories.aggregate(pipeline)
    return list(cursor)

def change_name_admin(old_name, password):
    cursor = db.admin.find({"name": old_name, 'password': password})
    return list(cursor)

def update_name_admin(old_name, new_name):
    db.admin.update({"name": old_name}, {"$set": {"name": new_name}})
