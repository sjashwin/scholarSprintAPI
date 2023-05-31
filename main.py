import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.quiz import Quiz
from routes import ping
# Get environment variables
mongo_host = os.getenv("REACT_APP_MONGO_HOST")
db_name = os.getenv("REACT_APP_DB")
collection_name = os.getenv("REACT_APP_COLLECTIONS")

# Connect to MongoDB
client = AsyncIOMotorClient(mongo_host)
db = client.Questions
collection = db.OneWord

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

@app.get("/quiz", response_model=Quiz)
async def createQuiz():
    # Fetch the first document
    first_document = await collection.find().to_list(2)
    # Convert ObjectId to string and return the document
    quiz = Quiz(time=10, questions=first_document)
    return quiz

@app.post("/create-room", response_model=Quiz)
async def createRoom():
    # Fetch the first document
    first_document = await collection.find().to_list(2)
    # Convert ObjectId to string and return the document
    quiz = Quiz(time=10, questions=first_document)
    return quiz