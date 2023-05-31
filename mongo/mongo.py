from pymongo import MongoClient
from typing import List, Any
import os

class MongoController:
    client: MongoClient
    DB: MongoClient
    COLLECTIONS: MongoClient
    Questions: List[Any]

    def __init__(self):
        print(os.getenv("REACT_APP_MONGO_HOST"))
        self.client = MongoClient(os.getenv("REACT_APP_MONGO_HOST"))
        self.DB = self.client[os.getenv("REACT_APP_DB")]
        self.COLLECTION = self.DB[os.getenv("REACT_APP_COLLECTIONS")]
        self.data = self.COLLECTION.find().limit(10)

    def getQuestions(self) -> list:
        return list(self.data)
