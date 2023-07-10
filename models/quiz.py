from pydantic import BaseModel, Field
from typing import Optional, List
from mongo.PyObjectId import PyObjectId

class Quiz(BaseModel):
    id: Optional[PyObjectId] = Field(default_factor=PyObjectId, alias='_id')
    time: int = Field(...) # Duration Given To Finish The Quiz.
    image: str = Field(...) # Image For The Quiz
    size: int = Field(...) # Number of Questions
    type: int = Field(...) # type of quiz 1. OneWord 3. TrueFalse
    name: str = Field(...) # Name of the Quiz
    domain: List[int] = Field(...) # Domain
    s: Optional[bool] # Seearch Required
    q: Optional[str] # Query to search
    quesID: Optional[List[str]]
    userID: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}