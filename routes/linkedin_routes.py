from fastapi import APIRouter
import requests
from pydantic import BaseModel
from fastapi import HTTPException
import os

router = APIRouter()

class User(BaseModel):
    userID: str
    name: str
    email: str

@router.post("/linkedin", response_model=User)
async def linkedin(data: dict):

    access_token = await getAccessToken(
        code=data.get('code'),
        uri=data.get('uri')
    )
    userInfo = await getProfile(access_token=access_token)
    print(userInfo)
    return userInfo

async def getAccessToken(code: str, uri: str)->str:
    url = 'https://www.linkedin.com/oauth/v2/accessToken'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': os.getenv("REACT_APP_LINKEDIN_CLIENT"),
        'client_secret': os.getenv("REACT_APP_LINKEDIN_SECRET"),
        'redirect_uri': uri
    }
    response = requests.post(url, headers=headers, data=params)
    if response.status_code == 200:
        return str(response.json()['access_token'])
    raise HTTPException(status_code=response.status_code, detail='Error getting Access Token')

async def getProfile(access_token: str) -> User:
    if not access_token:
        return
    url="https://api.linkedin.com/v2/me"
    profile_headers = {
        "Authorization": f'Bearer {access_token}',
        'x-li-format': 'json'
    }

    response = requests.get(url, headers=profile_headers)
    if response.status_code == 200:
        profile_data = response.json()
        profile_id = profile_data['id']
        name = profile_data['localizedFirstName'] + " " + profile_data['localizedLastName']
        email_url = f'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'
        email_headers = { 
            'Authorization': f'Bearer {access_token}',
            'x-li-format': 'json'
        }
        email_response = requests.get(email_url, headers=email_headers)

        if email_response.status_code == 200:
            email_data = email_response.json()
            email_address = email_data['elements'][0]['handle~']['emailAddress']
        else:
            raise HTTPException(status_code=email_response.status_code, detail='Error getting email')
    user = User(userID=profile_id, name=name, email=email_address) 
    return user
