from pydantic import BaseModel, Field
from typing import Optional, List
from mongo.PyObjectId import PyObjectId

class Quiz(BaseModel):
    id: Optional[PyObjectId] = Field(default_factor=PyObjectId, alias='_id')
    time: int = Field(...)
    image: str = Field(...)
    size: int = Field(...)
    type: int = Field(...)
    name: str = Field(...)
    domain: List[int] = Field(...)
    s: Optional[bool] = Field(...)
    q: Optional[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}