import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
DB_URI = os.getenv("MONGO_DATABASE")
database: any = MongoClient(DB_URI)
conn: any = database.idh_system
