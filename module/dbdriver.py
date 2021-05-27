import pymongo
from decouple import config

url = config('URL')
mongo = pymongo.MongoClient(url)
db = mongo.taxi_management