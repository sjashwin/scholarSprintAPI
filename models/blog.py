from pydantic import BaseModel, Field
from mongo.PyObjectId import PyObjectId
from typing import Optional, List
from datetime import datetime

class Blog(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    content: str = Field(...)
    date: datetime = Field(...)
    image: Optional[str] = Field(...)
    title: str = Field(...)
    keywords: List[str] = Field(...)
    tags: List[str] = Field(...)
    visited: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}