from fastapi import APIRouter, Request, HTTPException, status
from datetime import date
from mongo.mongo import USER_COLLECTION, PROGRESS_COLLECTION
import logging

router = APIRouter()

@router.post("/login")
async def login(data: dict):
    if data.get("email") == "" or data.get("email") is None:
        logging.error(f"Invlaid Email")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str("Invalid Email"))
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
            if userEmail == None or userEmail == "":
                return {"status": status.HTTP_403_FORBIDDEN, "result": "", "user": ""}
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
                "r": 1,
            }
            print("user", userInfo)
            result = await progress(userID)
            result = await USER_COLLECTION.insert_one(userInfo)
            userInfo["_id"] = str(userInfo["_id"])
            logging.info(f"New User {username} Logged In Successfully")
            return { "status": status.HTTP_200_OK, "result": str(result.inserted_id), "user": userInfo }
    except Exception as e:
        logging.error(f"Error Logging In Or Signin Up: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def progress(userID):
    data = {
        "uid": userID,
        "score": 10,
        "progress": [{}]
    }
    result = await PROGRESS_COLLECTION.insert_one(data)
    return str(result.inserted_id)