"""
utils folder containg
    send_email
    send_email_for_forgot_password
"""

import smtplib
from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.settings import settings

new_account_template_file_path = Path("app/email_templates/new_account_template.html")
forgot_password_template_file_path = Path(
    "app/email_templates/forgot_password_template.html"
)


def send_email(email: str, otp: str) -> None:
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

    with new_account_template_file_path.open(mode="r", encoding="utf-8") as file:
        template = file.read()
    email_body = template.replace("{{ otp }}", str(otp))
    msg.attach(MIMEText(email_body, "html"))

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())


# Function to send mail to user regarding forgot password


def send_email_for_forgot_password(email: str, otp: str) -> None:
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
    with forgot_password_template_file_path.open(mode="r", encoding="utf-8") as file:
        template = file.read()
    email_body = template.replace("{{ otp }}", str(otp))
    msg.attach(MIMEText(email_body, "html"))

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
