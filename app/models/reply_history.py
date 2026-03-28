from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class ReplyHistory(Base):
    __tablename__ = "reply_history"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"))
    generated_reply = Column(Text)
    edited_reply = Column(Text, nullable=True)
    sent_status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)