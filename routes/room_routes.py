from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Union, Optional
from user import User
from quiz import Quiz
import uuid
from datetime import datetime
from mongo.mongo import QUIZ_COLLECTION

class Result:
    i: int
    result: Union[int, str, bool]

class Room(BaseModel):
    id = str(uuid.uuid4())
    user: List[User]
    quiz: Quiz
    results: List[Result]
    userID: str
    expiry: Optional[datetime]
    invites: List[str]

QUESTION_LIMIT = 20

router = APIRouter()

rooms: List[Room] = []

async def fetch_quiz_by_domain():
    pipeline = [{'$match': {'domain': [1, 1]}}, {'$sample': {'size': 1}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(1)
    return doc

@router.post("/room/create")
async def createRoom(userID: str):
    quiz = await fetch_quiz_by_domain()
    newRoom = Room(
        user=[], 
        userID=userID, 
        results=[],
        quiz=quiz
    )
    rooms.append(newRoom)
    return newRoom.id

@router.delete("/room/delete/{roomID}")
async def deleteRoom(roomID: str):
    for r in rooms:
        if roomID == r.id:
            del r

@router.post("/room/invite")
async def invite(data: dict):
    roomID = data.get("roomID")
    email = data.get("email")
    for r in rooms:
        if r.id == roomID:
            r.invites.append(email)
            return True
    return False

@router.post("/room/access")
async def access(data: dict):
    email = data.get("email")
    roomID = data.get("roomID")
    for r in rooms:
        if r.id == roomID:
            return email in r.invites
    return False

@router.get("/question/{id}")
async def questions():
    pass

@router.post("/answer/{id}/{userID}")
async def answer(id: str, userID: str, answer: dict):
    pass

@router.post("/complete/{id}")
async def complete():
    pass