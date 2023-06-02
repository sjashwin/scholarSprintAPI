from fastapi import APIRouter
from typing import List
import os
from models.question import Question
from mongo.mongo import client


router = APIRouter()

@router.post("/create-room", response_model=List[Question], status_code=200)
async def createRoom():
    # Fetch the first document
    db_name = os.getenv("REACT_APP_DB")
    collection_name = os.getenv("REACT_APP_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    rooms = await collection.find().to_list(2)
    # Convert ObjectId to string and return the document
    return rooms
