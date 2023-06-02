from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import ping, room_routes, quiz_routes

# Create FastAPI instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with the appropriate frontend URL
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(room_routes.router)
app.include_router(quiz_routes.router)