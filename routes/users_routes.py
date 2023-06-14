from fastapi import APIRouter, Request, HTTPException, status
from datetime import date
import os
from mongo.mongo import client

router = APIRouter()

@router.post("/anonymousLogin")
async def anonymousLogin(request: Request, data: dict):
    try:
        db_name = os.getenv("REACT_APP_DB_QUIZ")
        db_collections = os.getenv("REACT_APP_USERS_COLLECTIONS")
        db=client[db_name]
        collection = db[db_collections]
        ip_address = request.client.host
        userID = data.get("userID")
        if userID is None or userID == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="userID is required")
        userEmail = data.get("email") or ""
        userPhone = data.get("phnone") or ""
        today = date.today().isoformat()
        data = { 
            "ip": ip_address, 
            "id": userID, 
            "date": today,
            "country": "IN",
            "visited": 1,
            "phone": userPhone,
            "email": userEmail,
            "email_v": False,
            "phone_v": False,
            "registered": False,
        }
        existing_data = await collection.find_one({"id": userID})
        if existing_data:
            # Increase the count of visited
            visited_count = existing_data.get("visited", 0)
            data["visited"] = visited_count + 1
            # Update the existing data
            collection.update_one({"id": userID}, {"$set": data})
        else:
            data["visited"] = 1
            # Insert the data into MongoDB collection
            collection.insert_one(data)
        return {"status": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/checkIP")
async def check_ip(request: Request):
    try:
        ip_address = request.client.host
        db_name = os.getenv("REACT_APP_DB_QUIZ")
        db_collections = os.getenv("REACT_APP_USERS_COLLECTIONS")
        db = client[db_name]
        collection = db[db_collections]

        existing_data = await collection.find_one({"ip": ip_address})
        if existing_data:
            # Update the visited count
            visited_count = existing_data.get("visited", 0) + 1
            existing_data["visited"] = visited_count
            # Update the existing data in the collection
            await collection.replace_one({"ip": ip_address}, existing_data)
            return existing_data
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))