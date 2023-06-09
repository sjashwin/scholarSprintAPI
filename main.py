from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routes import invite_routes, ping, quiz_routes, question_routes, session_routes, users_routes, feedback_routes
from routes import progress_routes, blog_routes, linkedin_routes, creator
from watchers.newQuiz_watcher import QuizAdd_watcher
import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create FastAPI instance
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="my_secret_key", same_site="none", https_only=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000", "http://localhost:3000", "https://scholar-sprint.vercel.app", "https://www.scholarsprint.app"],  # Replace with the appropriate frontend URL
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(quiz_routes.router)
app.include_router(question_routes.router)
app.include_router(session_routes.router)
app.include_router(users_routes.router)
app.include_router(progress_routes.router)
app.include_router(feedback_routes.router)
app.include_router(invite_routes.router)
app.include_router(blog_routes.router)
app.include_router(linkedin_routes.router)
app.include_router(creator.router)

logging.info("Server Started Successfully.")

#@app.on_event("startup")
#async def startup_event():
#    asyncio.create_task(QuizAdd_watcher())