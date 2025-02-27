from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import json

class Settings(BaseSettings):
    # Service settings
    ENVIRONMENT: str = "development"
    PORT: int = 8001
    
    # CORS settings
    CORS_ORIGINS: str = '["*"]'
    
    # Gmail API settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REFRESH_TOKEN: str
    
    # Email settings
    EMAIL_SENDER: str
    EMAIL_SENDER_NAME: str = "Task Manager"
    EMAIL_SERVICE_URL: str = "http://localhost:8001"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding='utf-8'
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["*"]

settings = Settings() 