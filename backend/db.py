
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGO_URI = "mongo url"

client = MongoClient(MONGO_URI)
db = client["myFirstDatabase"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    for doc in db["myFirstCollection"].find():
        print(doc)
except Exception as e:
    print(e)

def get_db():
    return db
