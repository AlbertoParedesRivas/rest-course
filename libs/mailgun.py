import os
from requests import Response, post
from typing import List

FAILED_LOAD_API_KEY = "Failed to load Mailgun API key"
FAILED_LOAD_DOMAIN = "Failed to load Mailgun domain"
ERROR_SENDING_EMAIL = "Error sending confirmation email."

class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Mailgun:

    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = "mailgun@sandbox50876514a9db4b92ac79d248958d0eba.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html:str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException(FAILED_LOAD_API_KEY)
        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException(FAILED_LOAD_DOMAIN)
        response = post(
            f"http://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api",cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} {cls.FROM_EMAIL}",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html
            }
        )
        
        if response.status_code is not 200:
            raise MailgunException(ERROR_SENDING_EMAIL)
        
        return response