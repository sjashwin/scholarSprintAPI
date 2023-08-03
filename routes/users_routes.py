from fastapi import APIRouter, Request, HTTPException, status
from datetime import date
from mongo.mongo import USER_COLLECTION, PROGRESS_COLLECTION
from bson import ObjectId
import logging

router = APIRouter()

@router.post("/login")
async def login(data: dict):
    try:
        userEmail = data.get("email")
        userPhone = data.get("phone") or ""
        userCountry = data.get("country") or ""
        userLanguage = data.get("language") or ""
        username=data.get("name")
        today=date.today().isoformat()
        existing_data = await USER_COLLECTION.find_one({"e": userEmail})
        if existing_data:
            existing_data["_id"] = str(existing_data["_id"])
            result_update = await USER_COLLECTION.update_one({"e": userEmail}, {"$inc": {"v": 1}})
            logging.info(f"User {username} Logged In Successfully")
            return { "status": status.HTTP_200_OK, "result": result_update.modified_count, "user": existing_data}
        else:
            userID=data.get("userID")
            userInfo={
                "id": userID, 
                "d": today,
                "c": userCountry,
                "l": userLanguage,
                "v": 1,
                "p": userPhone,
                "e": userEmail,
                "n": username,
                "email_v": False,
                "phone_v": False,
                "sub": 0,
                "sub_expiry": None,
            }
            result = await progress(userID)
            result = await USER_COLLECTION.insert_one(userInfo)
            userInfo["_id"] = str(userInfo["_id"])
            logging.info(f"New User {username} Logged In Successfully")
            return { "status": status.HTTP_200_OK, "result": str(result.inserted_id), "user": userInfo }
    except Exception as e:
        logging.error(f"{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def progress(userID):
    data = {
        "uid": userID,
        "score": 10,
        "progress": [{}]
    }
    result = await PROGRESS_COLLECTION.insert_one(data)
    return str(result.inserted_id)

@router.put("/updateUsername")
async def update_username(data: dict):
    try:
        user_id = data.get("id")
        new_username = data.get("name")
        if not user_id or not new_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Both 'id' and 'name' fields are required.")
        
        user_id = ObjectId(user_id)    
        existing_user = await USER_COLLECTION.find_one({"_id": user_id})
        if existing_user:
            result_update = await USER_COLLECTION.update_one({"_id": user_id}, {"$set": {"n": new_username}})
            if result_update.modified_count > 0:
                logging.info(f"Username for User ID {user_id} updated successfully.")
                return {"status": "success", "message": "Username updated successfully."}
            else:
                return {"status": "error", "message": "Failed to update the username."}
        else:
            raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        logging.error(f"{e}")
        raise HTTPException(status_code=500, detail=str(e))