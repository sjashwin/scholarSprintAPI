from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import secrets

router = APIRouter()

# Define the secret key used for token signing
SECRET_KEY = "your_secret_key"

# Define Pydantic models for payload and token
class Payload(BaseModel):
    email: str


class Token(BaseModel):
    token: str
    access_code: str
    room_id: str


@router.post("/generate_token", response_model=Token)
def generate_token(payload: Payload):
    # Generate the access code
    access_code = secrets.token_hex(4)

    # Calculate the token's expiration time
    expiration = datetime.utcnow() + timedelta(days=1)

    room_id = secrets.token_hex(8)

    # Create the token
    token_payload = payload.dict()
    token_payload["exp"] = expiration
    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    return Token(token=token, access_code=access_code, room_id=room_id)
