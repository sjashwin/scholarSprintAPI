"""
session_handling.py

This module provides FastAPI routes for setting and getting a username in a session.

Author: Ashwin Thinnappan
Email: ashwin@codseg.com
Date: 1 Jun 2023
"""

from fastapi import APIRouter, Request, HTTPException, status

router = APIRouter()

@router.get("/set-session/{username}")
async def set_session(username: str, request: Request):
    """
    Sets a session variable 'username' to the given value.
    
    This method tries to set the username in the session. If successful, it returns a success message. If
    it fails, it raises an HTTPException with a 500 status code.

    :param username: The username to be stored in the session.
    :param request: The incoming request, which contains the session object.
    :return: A dictionary containing a success message if the session variable was set successfully.
    :raises HTTPException: If there is an error setting the session variable.
    """
    try:
        request.session["username"] = username
        return {"message": "session set"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get-session")
async def get_session(request: Request):
    """
    Retrieves the 'username' from the current session.

    This method tries to get the username from the session. If the username exists, it returns the username. If 
    the username does not exist, it raises an HTTPException with a 404 status code.

    :param request: The incoming request, which contains the session object.
    :return: A dictionary containing the username if it is found in the session.
    :raises HTTPException: If there is no 'username' found in the session.
    """
    user_name = request.session.get("username")
    if user_name:
        return {"message": user_name}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active session")
