from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routes import ping, quiz_routes, question_routes, session_routes, users_routes, feedback_routes

# Create FastAPI instance
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="my_secret_key", same_site="none", https_only=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000", "http://localhost:3000", "https://scholar-sprint.vercel.app"],  # Replace with the appropriate frontend URL
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(quiz_routes.router)
app.include_router(question_routes.router)
app.include_router(session_routes.router)
app.include_router(users_routes.router)
app.include_router(feedback_routes.router)