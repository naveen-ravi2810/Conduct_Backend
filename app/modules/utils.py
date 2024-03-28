"""
utils folder containg
    send_otp
    send_otp_for_forgot_password
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery

from app.core.settings import settings


celery_app = Celery(
    "tasks", broker=settings.CELERY_BROKER, backend=settings.CELERY_BACKEND
)


# Function to verify the users email
@celery_app.task(name="Sending email for verification")
def send_otp(email: str, otp: str):
    """
    celery task to send email for verification
    """
    try:
        send_email(email, otp)
    except Exception as e:  # pylint: disable=W0718
        print(f"Failed to send OTP email to {email}: {e}")


def send_email(email: str, otp: str):
    """
    getting email and otp and sending to the respectivve user in the
    for email verification template
    """
    sender_email = settings.EMAIL_SENDER_ID
    sender_password = settings.EMAIL_SENDER_PASSWORD
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "OTP Verification"

    with open("app/modules/new_account_template.html", "r", encoding="utf-8") as file:
        template = file.read()
    email_body = template.replace("{{ otp }}", str(otp))
    msg.attach(MIMEText(email_body, "html"))

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())


# Function to send mail to user regarding forgot password
@celery_app.task(name="Sending email for forgot password")
def send_otp_for_forgot_password(email: str, otp: str):
    """
    celery task to send email for password change
    """
    try:
        send_email_for_forgot_password(email, otp)
    except Exception as e:  # pylint: disable=W0718
        print(f"Failed to send OTP email to {email}: {e}")


def send_email_for_forgot_password(email: str, otp: str):
    """
    getting email and otp and sending to the respectivve user in the
    forgot password template
    """
    sender_email = settings.EMAIL_SENDER_ID
    sender_password = settings.EMAIL_SENDER_PASSWORD
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Forgot password"
    with open(
        "app/modules/forgot_password_template.html", "r", encoding="utf-8"
    ) as file:
        template = file.read()
    email_body = template.replace("{{ otp }}", str(otp))
    msg.attach(MIMEText(email_body, "html"))

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
