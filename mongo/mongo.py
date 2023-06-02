import os
from motor.motor_asyncio import AsyncIOMotorClient

mongo_host = os.getenv("REACT_APP_MONGO_HOST")
client = AsyncIOMotorClient(mongo_host)
