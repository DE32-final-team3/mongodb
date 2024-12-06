from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:team3@localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "movies")

motor_client = AsyncIOMotorClient(MONGO_URI)

engine = AIOEngine(motor_client=motor_client, database=DATABASE_NAME)

