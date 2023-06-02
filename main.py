import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.quiz import Quiz
from routes import ping, room_routes
from typing import List
from models.question import Question
# Get environment variables
mongo_host = os.getenv("REACT_APP_MONGO_HOST")

# Connect to MongoDB
client = AsyncIOMotorClient(mongo_host)

# Create FastAPI instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with the appropriate frontend URL
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(room_routes.router)

@app.get("/quiz", response_model=List[Quiz])
async def createQuiz():
    # Fetch the first document
    db_name = os.getenv("REACT_APP_DB_QUIZ")
    collection_name = os.getenv("REACT_APP_QUIZ_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    first_document = await collection.find().to_list(10)
    # Convert ObjectId to string and return the document
    return first_document

@app.post("/create-room", response_model=List[Question])
async def createRoom():
    # Fetch the first document
    db_name = os.getenv("REACT_APP_DB")
    collection_name = os.getenv("REACT_APP_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    first_document = await collection.find().to_list(2)
    # Convert ObjectId to string and return the document
    return first_document