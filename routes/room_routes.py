from fastapi import APIRouter, HTTPException
from models.user import User
from models.room import RoomWarehouse


router = APIRouter()

@router.get("/rooms")
async def get_rooms():
    global RoomWarehouse
    return {"Rooms Open": RoomWarehouse}

@router.delete("/delete-room/{room_id}")
def delete_room(room_id: str):
    global RoomWarehouse
    rooms = [room for room in rooms if room.id != room_id]
    return {"message": "Room deleted successfully"}

@router.post("/join-room/{room_name}")
def join_room(room_name: str, user: User):
    global RoomWarehouse
    for room in RoomWarehouse:
        if room.id == room_name:
            if len(room.users) < 50:
                room.users.append(user)
                room.users[user.username] = 0  # Initialize user score
                return {"message": "User added to the room"}
            else:
                raise HTTPException(status_code=400, detail="Room is full")
    raise HTTPException(status_code=404, detail="Room not found")
