"""Email tasks module.

This module provides functions to send emails

Examples:
    To send email to a user:

Attributes:
    SMTP_HOST (str): The host of the smtp server
    SMTP_PORT (int): The port of the smtp server
"""

import smtplib
from email.message import EmailMessage

from logger import get_logger
from settings import settings
from src.auth.utils import create_access_token

logger = get_logger(__name__)


def get_verification_email_template(username: str, token: str) -> str:
    """Generate a HTML email template for user verification.

    Args:
        username (str): The username of the user.
        token (str): The token for verification.

    Returns:
        str: HTML email template.
    """
    return f"""
    <html>
    <head></head>
    <body>
        <p>Привет, {username}!</p>
        <a href="http://localhost:8000/auth/verify-email/?token={token}">
            Перейти по ссылке, чтобы подтвердить регистрацию
        </a>
    </body>
    </html>
    """


def get_email_message(username: str, email: str) -> EmailMessage:
    """Generate an email message for user verification.

    Args:
        username (str): The username of the user.
        email (str): The email address of the user.

    Returns:
        email.message.EmailMessage: The email message with the verification link.
    """
    email_message = EmailMessage()
    email_message["Subject"] = "Подтверждение регистрации"
    email_message["From"] = "verification_email_tempv@example.com"
    email_message["To"] = email

    token = create_access_token(data={"username": username, "email": email})
    template = get_verification_email_template(username, token)

    email_message.set_content(
        template,
        subtype="html",
    )
    return email_message


def send_email(username: str, email: str) -> None:
    """Send an email for user verification.

    Args:
        username (str): The username of the user.
        email (str): The email address of the user.

    Raises:
        smtplib.SMTPException: If there is an error sending the email.
        Exception: If there is an error in getting the email template or sending the email.
    """
    try:
        email = get_email_message(username=username, email=email)
        with smtplib.SMTP_SSL(host=settings.smtp.email_host, port=settings.smtp.email_port) as server:
            server.login(user=settings.smtp.email_user, password=settings.smtp.email_password)
            server.send_message(email)
    except smtplib.SMTPException as e:
        logger.error(f"Failed to send email to {email}. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"Failed to send email to {email}. Error: {e}")
        raise e
