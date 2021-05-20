import pymongo
mongo = pymongo.MongoClient('mongodb+srv://todoAppUser:Leanbichphuong0702@cluster0.oeozu.mongodb.net/TaxniManegement?retryWrites=true&w=majority')
db = mongo.taxi_management
# print(list(db.drivers.find({}, {"name": 1}))[0]['name'])
data = list(db.users.find({"email": 'aiden123@gmail.com'}))
print(data[0]['email'])