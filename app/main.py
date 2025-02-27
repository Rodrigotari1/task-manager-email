from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import email, tracking
import logging
import platform
import sys
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = FastAPI(
    title="Task Manager Email Service",
    description="Email microservice for Task Manager application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(email.router, prefix="/api/v1/email", tags=["email"])
app.include_router(tracking.router, prefix="/api/v1/tracking", tags=["tracking"])

# Add debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "Task Manager Email Service is running"}

@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint that provides detailed information about the email service
    and performs a basic SMTP connection test.
    """
    logger.debug("Health check endpoint called")
    
    # System information
    system_info = {
        "os": platform.system(),
        "python_version": sys.version,
        "timestamp": datetime.now().isoformat(),
    }
    
    # Email configuration (without sensitive data)
    email_config = {
        "smtp_server": settings.smtp_server,
        "smtp_port": settings.smtp_port,
        "sender_email": settings.sender_email,
        "use_tls": settings.use_tls,
        "use_ssl": settings.use_ssl,
    }
    
    # Test SMTP connection
    smtp_test = {"success": False, "message": ""}
    try:
        if settings.use_ssl:
            server = smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port)
        else:
            server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
            if settings.use_tls:
                server.starttls()
        
        server.login(settings.smtp_username, settings.smtp_password)
        smtp_test["success"] = True
        smtp_test["message"] = "SMTP connection successful"
        server.quit()
    except Exception as e:
        smtp_test["message"] = f"SMTP connection failed: {str(e)}"
        logger.error(f"SMTP connection test failed: {str(e)}")
    
    return {
        "status": "healthy" if smtp_test["success"] else "unhealthy",
        "system_info": system_info,
        "email_config": email_config,
        "smtp_test": smtp_test,
    } 