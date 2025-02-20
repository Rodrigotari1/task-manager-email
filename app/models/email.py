from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict
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
    metadata: Optional[Dict[str, str]] = None  # For tracking custom data
    tags: Optional[List[str]] = None  # For categorization

class EmailStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    FAILED = "failed"

class EmailEvent(BaseModel):
    event_type: EmailStatus
    timestamp: datetime
    metadata: Optional[Dict[str, str]] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

class EmailResponse(BaseModel):
    status: EmailStatus
    message_id: str
    timestamp: datetime
    tracking_id: Optional[str] = None
    events: List[EmailEvent] = []
    open_count: Optional[int] = 0
    click_count: Optional[int] = 0
    delivery_attempts: Optional[int] = 1

class EmailAnalytics(BaseModel):
    total_sent: int
    total_delivered: int
    total_opened: int
    total_clicked: int
    average_open_rate: float
    average_click_rate: float
    delivery_success_rate: float
    peak_times: List[datetime]
    common_failures: Dict[str, int]

class EmailStatusResponse(BaseModel):
    status: EmailStatus
    sent_at: datetime
    delivered_at: Optional[datetime] = None
    error: Optional[str] = None 