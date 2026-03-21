import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.config import settings

from fastapi import Request

router = APIRouter()

@router.get("/login")
def login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&scope=https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send"
        "&access_type=offline"
        "&prompt=consent"
    )

    return RedirectResponse(google_auth_url)

@router.get("/auth/callback")
def auth_callback(request: Request):
    code = request.query_params.get("code")

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()

    # For now just return token (later we will store in DB)
    return token_data