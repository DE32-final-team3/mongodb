from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:team3@localhost:27017/")
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:cine@3.37.94.149:27017/")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "cinetalk")

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_IP = os.getenv("DB_IP")
DB_PORT = os.getenv("DB_PORT")
DATABASE_URL = f"mongodb://root:{DB_PASSWORD}@{DB_IP}:{DB_PORT}"

# client = AsyncIOMotorClient(MONGO_URI)
client = AsyncIOMotorClient(DATABASE_URL)

engine = AIOEngine(client=client, database="cinetalk")
