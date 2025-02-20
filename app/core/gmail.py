from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from typing import Optional
import os
import pickle
import logging
import traceback

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_DIR = 'credentials'
TOKEN_PATH = os.path.join(CREDENTIALS_DIR, 'token.pickle')

class GmailService:
    def __init__(self):
        self.service = None
        self.credentials = None
        self._initialize_service()

    def _initialize_service(self):
        """Initialize the Gmail API service."""
        try:
            logger.debug("Initializing Gmail service")
            creds = None
            
            # Load credentials from token pickle file if it exists
            if os.path.exists(TOKEN_PATH):
                logger.debug("Found token.pickle file, loading credentials")
                try:
                    with open(TOKEN_PATH, 'rb') as token:
                        creds = pickle.load(token)
                    logger.debug("Successfully loaded credentials from token.pickle")
                except Exception as e:
                    logger.error(f"Error loading token.pickle: {e}")
                    logger.error(traceback.format_exc())

            # If credentials are not valid, refresh them or create new ones
            if not creds or not creds.valid:
                logger.debug("Credentials not valid, attempting to refresh or create new ones")
                if creds and creds.expired and creds.refresh_token:
                    logger.debug("Refreshing expired credentials")
                    try:
                        creds.refresh(Request())
                        logger.debug("Successfully refreshed credentials")
                    except Exception as e:
                        logger.error(f"Error refreshing credentials: {e}")
                        logger.error(traceback.format_exc())
                else:
                    logger.debug("Creating new credentials from refresh token")
                    try:
                        creds = Credentials(
                            None,
                            refresh_token=settings.GOOGLE_REFRESH_TOKEN,
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=settings.GOOGLE_CLIENT_ID,
                            client_secret=settings.GOOGLE_CLIENT_SECRET,
                        )
                        logger.debug("Successfully created new credentials")
                    except Exception as e:
                        logger.error(f"Error creating new credentials: {e}")
                        logger.error(traceback.format_exc())

                # Save the credentials for future use
                try:
                    with open(TOKEN_PATH, 'wb') as token:
                        pickle.dump(creds, token)
                    logger.debug("Successfully saved credentials to token.pickle")
                except Exception as e:
                    logger.error(f"Error saving token.pickle: {e}")
                    logger.error(traceback.format_exc())

            try:
                self.service = build('gmail', 'v1', credentials=creds)
                logger.debug("Successfully built Gmail service")
            except Exception as e:
                logger.error(f"Error building Gmail service: {e}")
                logger.error(traceback.format_exc())
                raise

        except Exception as e:
            logger.error(f"Error in _initialize_service: {e}")
            logger.error(traceback.format_exc())
            raise

    def create_message(self, to: str, subject: str, html_content: str) -> dict:
        """Create a message for an email."""
        try:
            logger.debug(f"Creating email message for recipient: {to}")
            message = MIMEMultipart('alternative')
            message['to'] = to
            message['from'] = f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_SENDER}>"
            message['subject'] = subject

            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            logger.debug("Successfully created email message")
            return {'raw': raw_message}
        except Exception as e:
            logger.error(f"Error creating message: {e}")
            logger.error(traceback.format_exc())
            raise

    async def send_message(self, to: str, subject: str, html_content: str) -> Optional[str]:
        """Send an email message."""
        try:
            logger.debug("Creating message")
            message = self.create_message(to, subject, html_content)
            
            logger.debug("Attempting to send message via Gmail API")
            sent_message = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            logger.info(f"Message sent successfully. Message ID: {sent_message.get('id')}")
            return sent_message.get('id')
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            logger.error(traceback.format_exc())
            return None

gmail_service = GmailService() 