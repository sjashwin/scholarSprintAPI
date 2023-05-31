from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

# Pydantic model
class Question(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    q: str
    a: List[str]
    d: List[int]
    w: str
    s: bool
    c: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}