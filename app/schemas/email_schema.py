from pydantic import BaseModel
from typing import Optional


class EmailResponse(BaseModel):
    id: str
    sender: str
    subject: str
    snippet: str
    category: str


class EmailDetailResponse(BaseModel):
    id: str
    subject: str
    sender: str
    body: str
    is_handled: bool
    reply: str


class CustomRequest(BaseModel):
    instruction: str
