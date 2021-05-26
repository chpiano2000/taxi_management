import pymongo
# from module.user import user

url = 'mongodb+srv://todoAppUser:Leanbichphuong0702@cluster0.oeozu.mongodb.net/TaxniManegement?retryWrites=true&w=majority'
mongo = pymongo.MongoClient(url)
db = mongo.taxi_management

######################## USER #####################################

def add_users(data):
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
