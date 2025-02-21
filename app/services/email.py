from datetime import datetime
from typing import Optional
from app.core.gmail import gmail_service
from app.models.email import EmailRequest, EmailResponse, EmailStatus, EmailEvent
from app.utils.template import render_template
from app.services.tracking import tracking_service
from app.core.config import settings
import traceback
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EmailService:
    async def send_task_email(self, email_request: EmailRequest) -> EmailResponse:
        """Send a task notification email with tracking."""
        try:
            logger.debug(f"Starting to send email to: {email_request.to}")
            
            # Generate tracking ID
            tracking_id = await tracking_service.create_tracking_id()
            
            # Record initial event
            await tracking_service.add_event(
                tracking_id,
                EmailEvent(
                    event_type=EmailStatus.PENDING,
                    timestamp=datetime.utcnow(),
                    metadata={"task_id": email_request.task_id}
                )
            )
            
            # Generate tracking pixel and links
            tracking_pixel = await tracking_service.generate_tracking_pixel(tracking_id)
            
            # Render the email template
            try:
                html_content = render_template(
                    "email_templates/task_notification.html",
                    task_title=email_request.task_title,
                    task_description=email_request.task_description,
                    priority=email_request.priority.value,
                    tracking_id=tracking_id,
                    tracking_url=settings.EMAIL_SERVICE_URL,
                    # Add HubSpot fields
                    hubspot_portal_id=email_request.hubspot_portal_id,
                    hubspot_contact_id=email_request.hubspot_contact_id,
                    hubspot_deal_id=email_request.hubspot_deal_id,
                    task_url=email_request.task_url or "#"
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
                
                # Record failure event
                await tracking_service.add_event(
                    tracking_id,
                    EmailEvent(
                        event_type=EmailStatus.FAILED,
                        timestamp=datetime.utcnow(),
                        metadata={"error": str(gmail_error)}
                    )
                )
                raise

            if message_id:
                # Record success event
                await tracking_service.add_event(
                    tracking_id,
                    EmailEvent(
                        event_type=EmailStatus.SENT,
                        timestamp=datetime.utcnow(),
                        metadata={"message_id": message_id}
                    )
                )
                
                logger.info(f"Email sent successfully with message_id: {message_id}")
                return EmailResponse(
                    status=EmailStatus.SENT,
                    message_id=message_id,
                    tracking_id=tracking_id,
                    timestamp=datetime.utcnow()
                )
            else:
                # Record failure event
                await tracking_service.add_event(
                    tracking_id,
                    EmailEvent(
                        event_type=EmailStatus.FAILED,
                        timestamp=datetime.utcnow(),
                        metadata={"error": "No message_id received"}
                    )
                )
                
                logger.error("Email sending failed - no message_id received")
                return EmailResponse(
                    status=EmailStatus.FAILED,
                    message_id="",
                    tracking_id=tracking_id,
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
        """Get the status of a sent email with tracking events."""
        try:
            events = await tracking_service.get_email_events(message_id)
            if not events:
                return None
                
            # Return the most recent status
            return events[-1].event_type
        except Exception as e:
            logger.error(f"Error getting email status: {e}")
            return None

email_service = EmailService() 