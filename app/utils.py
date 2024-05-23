"""
utils folder contain
    send_email
    send_email_for_forgot_password
"""

import smtplib
from pathlib import Path
from fastapi import HTTPException, status

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


from app.core.db import r_conn_rate_limiter


# Basic implementation of rate_limiter with redis_db
async def get_rate_limiter_status(ip: str):
    previous_count = await r_conn_rate_limiter.get(ip)
    if previous_count is None:
        await r_conn_rate_limiter.setex(
            name=ip, time=settings.RATE_LIMITER_MAX_TIME_IN_SEC, value=1
        )
    elif int(previous_count.decode("utf-8")) >= settings.MAX_REQUEST_RATE_LIMTER:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="too many requests"
        )
    else:
        await r_conn_rate_limiter.incr(ip)
