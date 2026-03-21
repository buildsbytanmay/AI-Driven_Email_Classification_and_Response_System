from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.config import settings

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