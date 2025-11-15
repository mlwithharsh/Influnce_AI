from fastapi import APIRouter , Request
import requests, os

router = APIRouter()
@router.get('/instagram')

def instagram_auth():
    app_id = os.getenv("INSTAGRAM_APP_ID")
    redirect = os.getenv("INSTAGRAM_REDIRECT_URI")
    auth_url = f"https://api.instagram.com/oauth/authorize?client_id={app_id}&redirect_uri={redirect}&scope=user_profile,user_media&response_type=code"
    return {"auth_url": auth_url}

@router.get('/auth/callback')
def instagram_callback(code:str):
    app_id = os.getenv("INSTAGRAM_APP_ID")
    secret = os.getenv("INSTAGRAM_SECRET")
    redirect = os.getenv("INSTAGRAM_REDIRECT_URI")
    token_url = "https://api.instagram.com/oauth/access_token"

    data = {
        "client_id": app_id,
        "client_secret": secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect,
    }

    res = requests.post(token_url, data=data)
    return res.json()