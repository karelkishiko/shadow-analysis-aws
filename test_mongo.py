from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")
print("URI loaded:", "YES" if uri else "NO")

client = MongoClient(uri)

print(client.admin.command("ping"))
print("MongoDB connected successfully")
