from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ping import router as PingRouter
from routes.room_routes import router as RoomRouter
from typing import List
from models.room import Room

app = FastAPI()

rooms: List[Room] = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(PingRouter)
app.include_router(RoomRouter)
