from pydantic import BaseModel
from typing import Optional
import uuid

class User(BaseModel):
    id: str = str(uuid.uuid4())
    firstName: str
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None
    subscripton: bool = False