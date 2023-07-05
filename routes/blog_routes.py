from fastapi import APIRouter, HTTPException
from mongo.mongo import BLOG_COLLECTION
import logging
from models.blog import Blog
from typing import List


router = APIRouter()


@router.get("/blog/{title}", response_model=Blog)
async def getBlog(title: str):
    blog = await BLOG_COLLECTION.find_one({"title": title})
    if not blog:
        logging.error("Invalid Blog Post Request")
        raise HTTPException(status_code=400, detail="Invalid blog request. Blog Not Found")
    logging.debug(f"Blog post request {title}")
    return blog

@router.get("/blog")
async def getBlogs():
    titles = []
    async for doc in BLOG_COLLECTION.find({}, {"title": 1, "date": 1, "_id": 0}):
        titles.append({"title": doc["title"], "date": doc["date"]})
    return titles