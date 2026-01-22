from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

# Charger les variables d’environnement
load_dotenv()

uri = os.getenv("MONGODB_URI")
db_name = os.getenv("MONGODB_DB")
col_name = os.getenv("MONGODB_COLLECTION")

print("Connecting to MongoDB...")

client = MongoClient(uri)
db = client[db_name]
col = db[col_name]

# Charger les données
data = list(col.find({}, {"_id": 0}))

df = pd.DataFrame(data)

print("\n--- DATA SAMPLE ---")
print(df.head())

print("\n--- STATISTICS ---")
print(df[["altitude", "azimuth", "shadow_mean"]].describe())
