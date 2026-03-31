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
def get_unread_emails(category: str = None):
    db = SessionLocal()

    # 🔹 STEP 1 — Get access token
    access_token = user_token.get("access_token")
    if not access_token:
        return {"error": "User not authenticated"}

    # 🔹 STEP 2 — Fetch from Gmail
    gmail = GmailService(access_token)
    fetched_emails = gmail.get_unread_emails()

    # 🔹 STEP 3 — Save new emails only
    for e in fetched_emails:
        existing = db.query(Email).filter(
            Email.gmail_message_id == e["id"]
        ).first()

        if not existing:
            # 👉 Classification
            text = f"{e['subject']} {e['snippet']}"
            result = classify_email(text)

            new_email = Email(
                gmail_message_id=e["id"],
                sender=e["sender"],
                subject=e["subject"],
                body=e["snippet"],
                category=result["category"],
                confidence=result["confidence"]
            )

            db.add(new_email)

    db.commit()

    # 🔹 STEP 4 — Apply filter
    query = db.query(Email).filter(Email.is_handled == False)

    if category:
        query = query.filter(Email.category == category)

    emails = query.order_by(Email.created_at.desc()).all()

    db.close()

    # 🔹 STEP 5 — Return
    return [
        {
            "id": e.gmail_message_id,
            "sender": e.sender,
            "subject": e.subject,
            "snippet": e.body,
            "category": e.category
        }
        for e in emails
    ]


@router.get("/emails/sent")
def get_sent_emails():
    db = SessionLocal()

    emails = db.query(Email).filter(Email.is_handled == True).all()

    db.close()

    return [
        {
            "id": e.gmail_message_id,
            "sender": e.sender,
            "subject": e.subject,
            "snippet": e.body,
            "category": e.category
        }
        for e in emails
    ]



@router.get("/emails/{id}")
def get_email(id: str):
    db = SessionLocal()   # ✅ FIX

    access_token = user_token.get("access_token")

    if not access_token:
        db.close()
        return {"error": "Not authenticated"}

    # 🔹 Gmail fetch
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

    # 🔹 Get email from DB
    email = db.query(Email).filter(Email.gmail_message_id == id).first()

    # 🔹 Default values (IMPORTANT)
    is_handled = False
    reply_text = ""

    if email:
        is_handled = email.is_handled
    
        reply = db.query(ReplyHistory).filter(
            ReplyHistory.email_id == email.id
        ).order_by(ReplyHistory.created_at.desc()).first()

        if reply:
            reply_text = reply.generated_reply

    db.close()   # ✅ FIX

    return {
        "id": id,
        "subject": subject,
        "sender": sender,
        "body": body,
        "is_handled": is_handled,
        "reply": reply_text
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



@router.post("/emails/{id}/mark-handled")
def mark_email_handled(id: str):
    db = SessionLocal()

    email = db.query(Email).filter(Email.gmail_message_id == id).first()

    if email:
        email.is_handled = True
        db.commit()

    db.close()

    return {"message": "Email marked as handled"}