from pydantic import BaseModel, Field
from typing import List, Optional
from mongo.PyObjectId import PyObjectId

class Question(BaseModel):
    id: Optional[PyObjectId] = Field(default_factor=PyObjectId, alias='_id')
    q: str = Field(...)
    a: str = Field(...)
    d: List[int] = Field(...)
    c: str = Field(...)
    t: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}