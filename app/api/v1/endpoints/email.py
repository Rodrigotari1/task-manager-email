from fastapi import APIRouter, HTTPException
from app.models.email import EmailRequest, EmailResponse, EmailStatusResponse, EmailStatus
from app.services.email import email_service
from datetime import datetime

router = APIRouter()

@router.post("/send", response_model=EmailResponse)
async def send_email(email_request: EmailRequest):
    """
    Send a task notification email.
    """
    try:
        response = await email_service.send_task_email(email_request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )

@router.get("/status/{message_id}", response_model=EmailStatusResponse)
async def get_email_status(message_id: str):
    """
    Get the status of a sent email.
    """
    try:
        status = await email_service.get_email_status(message_id)
        if status:
            return EmailStatusResponse(
                status=status,
                sent_at=datetime.utcnow(),  # In a real app, this would come from a database
                delivered_at=datetime.utcnow() if status == EmailStatus.DELIVERED else None
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Email with message_id {message_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get email status: {str(e)}"
        ) 