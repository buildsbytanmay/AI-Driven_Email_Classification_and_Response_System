from fastapi import APIRouter
from app.services.gmail_service import GmailService
from app.services.ai_classifier import classify_email
from app.services.ai_reply_generator import generate_ai_reply, generate_custom_reply
from app.routers.auth import user_token
from app.database import SessionLocal
from app.models.email import Email
from app.models.reply_history import ReplyHistory
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.services.gmail_service import get_body

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



@router.get("/emails/{id}")
def get_email(id: str):
    access_token = user_token.get("access_token")

    if not access_token:
        return {"error": "Not authenticated"}

    gmail = GmailService(access_token)

    service = gmail.get_unread_emails  # just to access service setup

    creds = Credentials(token=access_token)
    service = build("gmail", "v1", credentials=creds)

    msg = service.users().messages().get(
        userId="me",
        id=id,
        format="full"
    ).execute()

    body = get_body(msg["payload"])

    headers = msg["payload"]["headers"]

    subject = ""
    sender = ""

    for h in headers:
        if h["name"] == "Subject":
            subject = h["value"]
        if h["name"] == "From":
            sender = h["value"]

    return {
        "id": id,
        "subject": subject,
        "sender": sender,
        "body": body
    }



def extract_sender_name(sender: str):
    if "<" in sender:
        return sender.split("<")[0].strip()
    return sender.split("@")[0]



@router.post("/emails/{id}/generate-reply")
def generate_reply(id: str):
    db = SessionLocal()

    email = db.query(Email).filter(
        Email.gmail_message_id == id
    ).first()

    if not email:
        db.close()
        return {"error": "Email not found"}

    sender_name = extract_sender_name(email.sender)
    user_name = user_token.get("name", "User")

    reply = generate_ai_reply(
        email_text=email.body,
        sender_name=sender_name,
        user_name=user_name
    )

    # ✅ Save to history
    history = ReplyHistory(
        # email_id=email.gmail_message_id,
        email_id=email.id,
        generated_reply=reply
    )

    db.add(history)
    db.commit()

    db.close()

    return {"reply": reply}



from pydantic import BaseModel

class CustomRequest(BaseModel):
    instruction: str


@router.post("/emails/{id}/custom-reply")
def custom_reply(id: str, request: CustomRequest):
    db = SessionLocal()

    email = db.query(Email).filter(
        Email.gmail_message_id == id
    ).first()

    if not email:
        db.close()
        return {"error": "Email not found"}

    sender_name = extract_sender_name(email.sender)
    user_name = user_token.get("name", "User")

    reply = generate_custom_reply(
        email_text=email.body,
        instruction=request.instruction,
        sender_name=sender_name,
        user_name=user_name
    )

    # ✅ Save history
    history = ReplyHistory(
        # email_id=email.gmail_message_id,
        email_id=email.id,
        generated_reply=reply
    )

    db.add(history)
    db.commit()

    db.close()

    return {"reply": reply}