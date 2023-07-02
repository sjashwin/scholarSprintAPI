from fastapi import APIRouter, Request, HTTPException, status
from datetime import date
from mongo.mongo import USER_COLLECTION, PROGRESS_COLLECTION
import logging

router = APIRouter()

@router.post("/anonymousLogin")
async def anonymousLogin(request: Request, data: dict):
    try:
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
            "d": today,
            "c": "IN",
            "v": 1,
            "p": userPhone,
            "e": userEmail,
            "email_v": False,
            "phone_v": False,
            "r": False,
        }
        existing_data = await USER_COLLECTION.find_one({"id": userID})
        if existing_data:
            # Increase the count of visited
            visited_count = existing_data.get("visited", 0)
            data["visited"] = visited_count + 1
            # Update the existing data
            USER_COLLECTION.update_one({"id": userID}, {"$set": data})
        else:
            data["visited"] = 1
            # Insert the data into MongoDB collection
            USER_COLLECTION.insert_one(data)
        return {"status": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/login")
async def login(request: Request, data: dict):
    try:
        userEmail = data.get("email") or ""
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
            }
            result = await progress(userID)
            result = await USER_COLLECTION.insert_one(userInfo)
            userInfo["_id"] = str(userInfo["_id"])
            logging.info(f"New User {username} Logged In Successfully")
            return { "status": status.HTTP_200_OK, "result": str(result.inserted_id), "user": userInfo }
    except Exception as e:
        logging.error(f"{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/checkIP")
async def check_ip(request: Request):
    try:
        ip_address = request.client.host

        existing_data = await USER_COLLECTION.find_one({"ip": ip_address})
        if existing_data:
            # Update the visited count
            visited_count = existing_data.get("visited", 0) + 1
            existing_data["visited"] = visited_count
            # Update the existing data in the collection
            await USER_COLLECTION.replace_one({"ip": ip_address}, existing_data)
            return existing_data
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def progress(userID):
    data = {
        "uid": userID,
        "score": 10,
        "progress": [{}]
    }
    result = await PROGRESS_COLLECTION.insert_one(data)
    return str(result.inserted_id)