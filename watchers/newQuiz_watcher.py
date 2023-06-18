from mongo.mongo import client
import os

async def QuizAdd_watcher():
    db_name = os.getenv("REACT_APP_DB_QUIZ")
    db_collections = os.getenv("REACT_APP_QUIZ_COLLECTIONS")
    db = client[db_name]
    collection = db[db_collections]
    try:
        print("Watcher started.")
        async with  collection.watch([{ "$match": {"operationType": "insert"}}]) as stream:
            async for insert_change in stream:
                print(f"new document: {insert_change['fullDocument']}")
    except Exception as e:
        print(f"Error in change stream, {str(e)}")