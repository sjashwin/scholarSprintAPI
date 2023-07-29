from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from models.quiz import Quiz
from models.question import Question
from uuid import uuid4
from mongo.mongo import QUIZ_COLLECTION, QUESTION_COLLECTION
from typing import Union

router = APIRouter()

class SocketResponse(BaseModel):
    type: str
    details: Union[str, Quiz, Question]

class Result(BaseModel):
    index: int
    answer: str
    score: int

class Manager():
    def __init__(self):
        self.users: set[str] = set()
        self.activeConnection: list[WebSocket] = []
        self.results: dict[str, list[Result]] = {}

    async def connect(self, websocket: WebSocket, email: str):
        await websocket.accept()
        print("Connecting", email)
        self.activeConnection.append(websocket)
        if email not in self.users:
            self.users.add(email)
            self.results[email] = [Result]
            response = SocketResponse(type="connected", details=f"{email} successfully connected.")
        else:
            response = SocketResponse(type="error", details=f"{email} is already in the room.")
            self.activeConnection.remove(websocket)
        await websocket.send_json(response.dict())
    
    def disconnect(self, websocket: WebSocket, email: str):
        print("Disconnecting")
        self.activeConnection.remove(websocket)
        self.users.remove(email)
    
    async def broadcast(self, message: str):
        for connection in self.activeConnection:
            await connection.send_text(message)

class Room(BaseModel):
    id: str = str(uuid4())
    quiz: Quiz
    invites: dict[str, bool] = ["sjashwin@live.in", "balathinnappan@gmail.com"]
    manager: Manager = Manager() # Socket Manager

    class Config:
        arbitrary_types_allowed = True

rooms: dict[str, Room] = {}

async def fetch_quiz_by_domain() -> Quiz:
    pipeline = [{'$match': {'domain': [1, 1]}}, {'$sample': {'size': 1}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(1)
    quiz = Quiz(
        _id=doc[0]['_id'],
        time=doc[0]['time'],
        image=doc[0]['image'],
        size=doc[0]['size'],
        type=doc[0]['type'],
        domain=doc[0]['domain'],
        s=doc[0]['s'],
        q=doc[0]['q'],
        quesID=None,
        userID=None,
        name=doc[0]['name']
    )
    return quiz

@router.get("/room/create")
async def create():
    quiz = await fetch_quiz_by_domain()
    room = Room(
        quiz=quiz,
    )
    rooms[str(room.id)] = room
    return room.id

@router.websocket("/room/{room_id}/{email}")
async def connect(websocket: WebSocket, room_id: str, email: str):
    currentRoom = rooms.get(room_id)
    if currentRoom is None:
        socket = SocketResponse(type="error", details="Invalid Room")
        await websocket.accept()
        await websocket.send_json(socket.dict())
        websocket.close(reason='Invalid Room')
        return 
    if email not in currentRoom.invites:
        socket = SocketResponse(type="error", details="Invalid Email")
        await websocket.accept()
        await websocket.send_json(socket.dict())
        websocket.close(reason='Invalid Email')
        return 
    manager = currentRoom.manager
    await manager.connect(websocket, email)
    
    if email not in currentRoom.invites:
        socket = SocketResponse(type="error", details="Private room. Not a valid invite.")
        await websocket.send_json(socket.dict())
        websocket.close()
        return
    try:
        while True:
            data = await websocket.receive_json()
            print(data["type"])
            if data['type'] == "quiz":
                resp = SocketResponse(type="quiz", details=currentRoom.quiz)
                await websocket.send_json(resp.dict())
    except WebSocketDisconnect:
        manager.disconnect(websocket, email)
        await manager.broadcast(f'{email} has disconnected.')

async def getQuiz() -> list[Question]:
    quiz = await QUESTION_COLLECTION.find({'d': [1, 2]}).to_list(10)
    return quiz

@router.websocket('/room/validate/{roomID}/{email}')
async def quizManager(websocket: WebSocket, roomID: str, email: str):
    currentRoom: Room = rooms.get(roomID)
    
    if currentRoom is None:
        await websocket.accept()
        socket = SocketResponse(type="quiz", details="Invalid room")
        await websocket.send_json(socket.dict())
        websocket.close(reason="Invalid Room")
    else:
        if websocket not in currentRoom.manager.activeConnection:
            await currentRoom.manager.connect(websocket=websocket, email=email)
        questions: list[Question] = await getQuiz()
        await websocket.send_json(SocketResponse(type="question", details=questions[0]["q"]).dict())
        try:
            while True:
                data = await websocket.receive_json()
                if data['type'] == "validate":
                    try:
                        index = data['index']
                        score = await check(data['answer'], questions[index]["a"])
                        result = Result(index=index, answer=data['answer'], score=score)
                        currentRoom.manager.results[email].append(result)
                    except IndexError:
                        pass 
                elif data["type"] == "question":
                    index = data["index"]
                    try:
                        response = SocketResponse(type="question", details=questions[index]["q"])
                        await websocket.send_json(response.dict())
                    except IndexError:
                        print("Quiz Complete")
                        response = SocketResponse(type="complete", details="Submitted Quiz")
                        await websocket.send_json(response.dict()) 
        except WebSocketDisconnect:
            try:
                currentRoom.manager.disconnect(websocket, email)
            except ValueError:
                pass

async def check(give: str, expected: str)->int:
    return 1 if give == expected else 0 
