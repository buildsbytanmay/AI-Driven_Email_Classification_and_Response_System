from fastapi import APIRouter
from app.services.gmail_service import GmailService
from app.services.ai_classifier import classify_email
from app.routers.auth import user_token
from app.database import SessionLocal
from app.models.email import Email
from datetime import datetime

router = APIRouter()

@router.get("/emails/unread")
def get_unread_emails():
    access_token = user_token.get("access_token")

    if not access_token:
        return {"error": "User not authenticated"}

    gmail_service = GmailService(access_token)
    emails = gmail_service.get_unread_emails()

    db = SessionLocal()

    result = []

    for e in emails:
        # Check if email already exists
        existing = db.query(Email).filter(
            Email.gmail_message_id == e["id"]
        ).first()

        if existing:
            # reuse classification
            result.append({
                "id": e["id"],
                "sender": e["sender"],
                "subject": e["subject"],
                "snippet": e["snippet"],
                "date": e["date"],
                "category": existing.category,
                "confidence": existing.confidence
            })
        else:
            # classify email
            text = f"{e['subject']} {e['snippet']}"
            classification = classify_email(text)

            # save in DB
            new_email = Email(
                gmail_message_id=e["id"],
                sender=e["sender"],
                subject=e["subject"],
                body=e["snippet"],
                category=classification["category"],
                confidence=classification["confidence"],
                received_at=datetime.utcnow()
            )

            db.add(new_email)
            db.commit()

            result.append({
                "id": e["id"],
                "sender": e["sender"],
                "subject": e["subject"],
                "snippet": e["snippet"],
                "date": e["date"],
                "category": classification["category"],
                "confidence": classification["confidence"]
            })

    db.close()
    return result