import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

database_url = os.getenv("DATABASE_URL")

print(database_url)

client = pymongo.MongoClient(database_url)
db = client.sample_mflix
collection = db.movies

items = collection.find().limit(5)

for item in items:
    print(item)
