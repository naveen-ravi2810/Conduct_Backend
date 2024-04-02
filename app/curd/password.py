from uuid import uuid4
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from redis.asyncio import Redis

from app.models import Users
from app.celery_worker import send_otp_for_forgot_password
from app.schema import ChangePasswordSchema, TokenResponse, NewPasswordSchema
from app.core.security import check_password, hash_password


# If the user forgot the password send the email to the particular user by his email id
async def send_email_otp_to_change_password(
    email: str, session: AsyncSession, r_conn: Redis
):
    try:
        statement = select(Users).where(Users.email == email)
        user = (await session.exec(statement)).one_or_none()
        if not user:
            raise ValueError("No user Found")
        otp = str(uuid4().int)[-6:]
        send_otp_for_forgot_password.delay(email=email, otp=otp)
        await r_conn.setex(
            name=f"forgot_password_otp:{user.email}", value=otp, time=600
        )
        return "OTP send Successfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Once the user get the email he can send new_password and otp to set the new_password
async def update_password_by_email_otp(
    session: AsyncSession, email: str, r_conn: Redis, new_password: NewPasswordSchema
):
    try:
        encoded_otp = await r_conn.get(name=f"forgot_password_otp:{email}")
        if encoded_otp is None:
            raise ValueError("Not password change request found")
        if encoded_otp.decode("utf-8") != str(new_password.otp):
            raise ValueError("Invalid OTP")
        statement = select(Users).where(Users.email == email)
        user = (await session.exec(statement=statement)).one_or_none()
        if not user:
            raise ValueError("User Not Exist")
        user.password = hash_password(new_password.new_password)
        session.add(user)
        await session.commit()
        await r_conn.delete(f"forgot_password_otp:{user.email}")
        return "PASSWORD UPDATED SUCCESSFULLY"
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# Hence the both the new passwords aare same now chck the old password
async def change_password_by_old_password(
    password: ChangePasswordSchema, session: AsyncSession, token: TokenResponse
):
    try:
        statement = select(Users).where(Users.email == token.email)
        user = (await session.exec(statement)).one_or_none()
        if not user:
            raise ValueError("No user found")
        if not check_password(
            password=password.old_password, hashed_password=user.password
        ):
            raise ValueError("Invalid Old Password")
        user.password = hash_password(password=password.new_password)
        session.add(user)
        await session.commit()
        return "PASSWORD CHANGED SUCCESSFULLY"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
