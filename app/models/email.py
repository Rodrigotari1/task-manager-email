from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class Priority(int, Enum):
    HIGHEST = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    LOWEST = 5

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    task_id: str
    task_title: str
    task_description: str
    priority: Priority

class EmailStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"

class EmailResponse(BaseModel):
    status: EmailStatus
    message_id: str
    timestamp: datetime

class EmailStatusResponse(BaseModel):
    status: EmailStatus
    sent_at: datetime
    delivered_at: Optional[datetime] = None
    error: Optional[str] = None 