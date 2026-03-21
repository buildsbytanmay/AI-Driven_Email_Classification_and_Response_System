from fastapi import APIRouter
from app.services.gmail_service import GmailService
from app.routers.auth import user_token

router = APIRouter()

@router.get("/emails/unread")
def get_unread_emails():
    access_token = user_token.get("access_token")

    if not access_token:
        return {"error": "User not authenticated"}

    gmail_service = GmailService(access_token)
    emails = gmail_service.get_unread_emails()

    return emails