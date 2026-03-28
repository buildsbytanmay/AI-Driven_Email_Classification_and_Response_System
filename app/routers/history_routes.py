from fastapi import APIRouter
from app.database import SessionLocal
from app.models.reply_history import ReplyHistory

router = APIRouter()


@router.get("/history")
def get_history():
    db = SessionLocal()

    history = db.query(ReplyHistory).all()

    db.close()

    return [
        {
            "email_id": h.email_id,
            "reply": h.generated_reply,
            "created_at": h.created_at
        }
        for h in history
    ]