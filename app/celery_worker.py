"""
Celery worker file
"""

import logging
from celery import Celery

from app.utils import send_email, send_email_for_forgot_password
from app.core.settings import settings

celery_app = Celery(
    "tasks", broker=settings.CELERY_BROKER, backend=settings.CELERY_BACKEND
)

logger = logging.getLogger(__name__)


# Function to verify the users email
@celery_app.task(name="Sending email for verification")
def send_otp(email: str, otp: str):
    """
    celery task to send email for verification
    """
    try:
        print("Hello world")
        send_email(email, otp)
    except Exception as e:  # pylint: disable=W0718
        logger.exception("Failed to send OTP email to %s: %s", email, e)


@celery_app.task(name="Sending email for forgot password")
def send_otp_for_forgot_password(email: str, otp: str):
    """
    celery task to send email for password change
    """
    try:
        send_email_for_forgot_password(email, otp)
    except Exception as e:  # pylint: disable=W0718
        logger.exception(
            "Failed to send OTP email for forgot password to %s: %s", email, e
        )
