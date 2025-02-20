from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import email

app = FastAPI(
    title="Task Manager Email Service",
    description="Email microservice for Task Manager application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(email.router, prefix="/api/v1/email", tags=["email"])

# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "Task Manager Email Service is running"} 