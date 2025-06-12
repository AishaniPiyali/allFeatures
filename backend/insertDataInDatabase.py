
import json
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://findthelost:Aishani20piyali@cluster0.ldzebp5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["myFirstDatabase"]
collection = db["products"]

# 👉 Ensure 'id' is unique before inserting
try:
    collection.create_index("id", unique=True)
except Exception as e:
    print("Index creation warning:", e)

# Load JSON file
with open("D:\\Angular Projects\\allFeatures\\ui\\public\\smartwatch.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # Should return a list of dicts

# Insert into MongoDB
try:
    collection.insert_many(data, ordered=False)  # ordered=False to continue on duplicates
    print("Data inserted successfully!")
except Exception as e:
    print("Insert failed:", e)

