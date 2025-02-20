from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from datetime import datetime
from app.services.tracking import tracking_service
from app.models.email import EmailEvent, EmailStatus, EmailAnalytics
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/track/{tracking_id}/pixel")
async def track_open(tracking_id: str, request: Request):
    """Track email opens via a 1x1 transparent pixel."""
    try:
        await tracking_service.add_event(
            tracking_id,
            EmailEvent(
                event_type=EmailStatus.OPENED,
                timestamp=datetime.utcnow(),
                user_agent=request.headers.get("user-agent"),
                ip_address=request.client.host,
                metadata={"source": "pixel"}
            )
        )
        logger.info(f"Open event recorded for email {tracking_id}")
    except Exception as e:
        logger.error(f"Error tracking email open: {e}")

    # Return a 1x1 transparent GIF
    return Response(
        content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b",
        media_type="image/gif"
    )

@router.get("/track/{tracking_id}/redirect")
async def track_click(tracking_id: str, url: str, request: Request):
    """Track email link clicks and redirect to the original URL."""
    try:
        await tracking_service.add_event(
            tracking_id,
            EmailEvent(
                event_type=EmailStatus.CLICKED,
                timestamp=datetime.utcnow(),
                user_agent=request.headers.get("user-agent"),
                ip_address=request.client.host,
                metadata={"clicked_url": url}
            )
        )
        logger.info(f"Click event recorded for email {tracking_id}")
    except Exception as e:
        logger.error(f"Error tracking email click: {e}")

    return RedirectResponse(url=url)

@router.get("/analytics")
async def get_analytics(days: int = 30) -> EmailAnalytics:
    """Get email analytics for the specified time range."""
    try:
        return await tracking_service.get_analytics({"days": days})
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise

@router.get("/events/{tracking_id}")
async def get_email_events(tracking_id: str):
    """Get all events for a specific email."""
    try:
        events = await tracking_service.get_email_events(tracking_id)
        return {"tracking_id": tracking_id, "events": events}
    except Exception as e:
        logger.error(f"Error getting email events: {e}")
        raise 