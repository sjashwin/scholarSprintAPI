import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Get environment variables
mongo_host = os.getenv("REACT_APP_MONGO_HOST")
db_name = os.getenv("REACT_APP_DB")
collection_name = os.getenv("REACT_APP_COLLECTIONS")

# Connect to MongoDB
client = AsyncIOMotorClient(mongo_host)
db = client.Questions
collection = db.OneWord
# Define the model
class Questions(BaseModel):
    id: Optional[PyObjectId] = Field(default_factor=PyObjectId, alias='_id')
    q: str = Field(...)
    a: List[str] = Field(...)
    d: List[int] = Field(...)
    w: str = Field(...)
    s: bool = Field(...)
    c: str = Field(...)
    t: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
    
class Quiz(BaseModel):
    time: int
    questions: List[Questions]

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

@app.get("/ping")
async def ping():
    return {"message": "pong for localhost"}
