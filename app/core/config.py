from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Service settings
    ENVIRONMENT: str = "development"
    PORT: int = 8001
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    
    # Gmail API settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REFRESH_TOKEN: str
    
    # Email settings
    EMAIL_SENDER: str
    EMAIL_SENDER_NAME: str = "Task Manager"
    
    # Email Service URL
    EMAIL_SERVICE_URL: str = "http://localhost:8002"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding='utf-8'
    )

settings = Settings() 