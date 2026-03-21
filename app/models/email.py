from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import Float
from datetime import datetime
from app.database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    gmail_message_id = Column(String, unique=True, index=True)
    sender = Column(String)
    subject = Column(String)
    body = Column(Text)
    category = Column(String, default="Uncategorized")
    confidence = Column(Float, nullable=True)
    received_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)