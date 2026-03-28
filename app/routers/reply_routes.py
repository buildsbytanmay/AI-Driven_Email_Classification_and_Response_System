from fastapi import APIRouter
from pydantic import BaseModel
from app.database import SessionLocal
from app.models.email import Email
from app.routers.auth import user_token
from app.services.ai_reply_generator import generate_ai_reply, generate_custom_reply

router = APIRouter()


class EmailRequest(BaseModel):
    email_id: str


@router.post("/reply/auto")
def auto_reply(request: EmailRequest):
    db = SessionLocal()

    # 1. Get email from DB
    email = db.query(Email).filter(
        Email.gmail_message_id == request.email_id
    ).first()

    if not email:
        db.close()
        return {"error": "Email not found"}

    # 2. Extract sender name
    sender = email.sender
    if "<" in sender:
        sender_name = sender.split("<")[0].strip()
    else:
        sender_name = sender.split("@")[0]

    # 3. Get user name (from Google login)
    user_name = user_token.get("name", "User")

    # 4. Generate reply
    reply = generate_ai_reply(
        email_text=email.body,
        sender_name=sender_name,
        user_name=user_name
    )

    db.close()

    return {"reply": reply}

class CustomReplyRequest(BaseModel):
    email_id: str
    instruction: str

    from app.services.ai_reply_generator import generate_custom_reply

@router.post("/reply/custom")
def custom_reply(request: CustomReplyRequest):
    db = SessionLocal()

    # 1. Fetch email from DB
    email = db.query(Email).filter(
        Email.gmail_message_id == request.email_id
    ).first()

    if not email:
        db.close()
        return {"error": "Email not found"}

    # 2. Extract sender name
    sender = email.sender
    if "<" in sender:
        sender_name = sender.split("<")[0].strip()
    else:
        sender_name = sender.split("@")[0]

    # 3. Get user name
    user_name = user_token.get("name", "User")

    # 4. Generate custom reply
    reply = generate_custom_reply(
        email_text=email.body,
        instruction=request.instruction,
        sender_name=sender_name,
        user_name=user_name
    )

    db.close()

    return {"reply": reply}