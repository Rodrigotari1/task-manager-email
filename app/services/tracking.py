from datetime import datetime
import uuid
from typing import Optional, Dict, List
from app.models.email import EmailEvent, EmailAnalytics, EmailStatus
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailTrackingService:
    def __init__(self):
        """Initialize tracking service."""
        self._events = {}  # In-memory store for development
    
    async def create_tracking_id(self) -> str:
        """Generate a unique tracking ID for an email."""
        tracking_id = str(uuid.uuid4())
        self._events[tracking_id] = []
        return tracking_id

    async def add_event(self, tracking_id: str, event: EmailEvent) -> bool:
        """Record an email event."""
        try:
            if tracking_id not in self._events:
                self._events[tracking_id] = []
            
            self._events[tracking_id].append(event)
            logger.info(f"Email event recorded for {tracking_id}: {event.event_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error recording email event: {e}")
            return False

    async def get_email_events(self, tracking_id: str) -> List[EmailEvent]:
        """Get all events for a specific email."""
        try:
            return self._events.get(tracking_id, [])
        except Exception as e:
            logger.error(f"Error fetching email events: {e}")
            return []

    async def get_analytics(self, time_range: Optional[Dict] = None) -> EmailAnalytics:
        """Get email analytics."""
        try:
            total_sent = sum(1 for events in self._events.values() 
                           if any(e.event_type == EmailStatus.SENT for e in events))
            total_opened = sum(1 for events in self._events.values() 
                             if any(e.event_type == EmailStatus.OPENED for e in events))
            total_clicked = sum(1 for events in self._events.values() 
                              if any(e.event_type == EmailStatus.CLICKED for e in events))
            
            return EmailAnalytics(
                total_sent=total_sent,
                total_delivered=total_sent,  # Assuming all sent are delivered for now
                total_opened=total_opened,
                total_clicked=total_clicked,
                average_open_rate=total_opened/total_sent if total_sent > 0 else 0,
                average_click_rate=total_clicked/total_sent if total_sent > 0 else 0,
                delivery_success_rate=1.0,  # Assuming 100% delivery for now
                peak_times=[datetime.utcnow()],
                common_failures={}
            )
        except Exception as e:
            logger.error(f"Error generating analytics: {e}")
            raise

    async def generate_tracking_pixel(self, tracking_id: str) -> str:
        """Generate a tracking pixel URL."""
        return f"{settings.EMAIL_SERVICE_URL}/api/v1/tracking/track/{tracking_id}/pixel"

    async def generate_tracking_link(self, tracking_id: str, original_url: str) -> str:
        """Generate a tracking link."""
        return f"{settings.EMAIL_SERVICE_URL}/api/v1/tracking/track/{tracking_id}/redirect?url={original_url}"

tracking_service = EmailTrackingService() 