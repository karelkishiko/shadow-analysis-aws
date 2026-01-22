import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB", "shadow_db")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "shadow_results")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
shadow_collection = db[COLLECTION_NAME]

