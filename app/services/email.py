from datetime import datetime
from typing import Optional
from app.core.gmail import gmail_service
from app.models.email import EmailRequest, EmailResponse, EmailStatus
from app.utils.template import render_template
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EmailService:
    async def send_task_email(self, email_request: EmailRequest) -> EmailResponse:
        """Send a task notification email."""
        try:
            logger.debug(f"Starting to send email to: {email_request.to}")
            
            # Render the email template
            try:
                html_content = render_template(
                    "email_templates/task_notification.html",
                    task_title=email_request.task_title,
                    task_description=email_request.task_description,
                    priority=email_request.priority.value
                )
                logger.debug("Template rendered successfully")
            except Exception as template_error:
                logger.error(f"Template rendering error: {template_error}")
                logger.error(traceback.format_exc())
                raise

            # Send the email
            try:
                logger.debug("Attempting to send email via Gmail service")
                message_id = await gmail_service.send_message(
                    to=email_request.to,
                    subject=email_request.subject,
                    html_content=html_content
                )
                logger.debug(f"Gmail service response - message_id: {message_id}")
            except Exception as gmail_error:
                logger.error(f"Gmail service error: {gmail_error}")
                logger.error(traceback.format_exc())
                raise

            if message_id:
                logger.info(f"Email sent successfully with message_id: {message_id}")
                return EmailResponse(
                    status=EmailStatus.SENT,
                    message_id=message_id,
                    timestamp=datetime.utcnow()
                )
            else:
                logger.error("Email sending failed - no message_id received")
                return EmailResponse(
                    status=EmailStatus.FAILED,
                    message_id="",
                    timestamp=datetime.utcnow()
                )

        except Exception as e:
            logger.error(f"Error in send_task_email: {str(e)}")
            logger.error(traceback.format_exc())
            return EmailResponse(
                status=EmailStatus.FAILED,
                message_id="",
                timestamp=datetime.utcnow()
            )

    async def get_email_status(self, message_id: str) -> Optional[EmailStatus]:
        """Get the status of a sent email."""
        # In a real implementation, you would query Gmail API or a database
        # For now, we'll return a mock status
        return EmailStatus.DELIVERED

email_service = EmailService() 