from pydantic import BaseModel
from datetime import datetime


class EmailRequest(BaseModel):
    email_id: str


class CustomReplyRequest(BaseModel):
    email_id: str
    instruction: str


class ReplyResponse(BaseModel):
    reply: str


class HistoryResponse(BaseModel):
    email_id: int
    reply: str
    created_at: datetime
