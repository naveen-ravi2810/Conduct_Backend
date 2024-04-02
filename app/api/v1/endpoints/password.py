from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_session, r_conn
from app.core.security import get_user_credentials
from app.schema import TokenResponse, ChangePasswordSchema, NewPasswordSchema
from app.curd.password import (
    send_email_otp_to_change_password,
    change_password_by_old_password,
    update_password_by_email_otp,
)

router = APIRouter()


@router.get("/forgot_password/{email}")
async def forgot_password(email: str, session: AsyncSession = Depends(get_session)):
    return await send_email_otp_to_change_password(
        email=email, session=session, r_conn=r_conn
    )


@router.post("/change_forgot_password/{email}")
async def change_forgot_password(
    email: str,
    new_password: NewPasswordSchema,
    session: AsyncSession = Depends(get_session),
):
    if new_password.new_password != new_password.re_enter_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password Mismatch"
        )
    return await update_password_by_email_otp(
        session=session, email=email, new_password=new_password, r_conn=r_conn
    )


@router.post("/change_password")
async def change_password(
    password: ChangePasswordSchema,
    token: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    if password.new_password != password.re_enter_new_password:
        raise HTTPException(
            detail="new_password and re-enter password are not same",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return await change_password_by_old_password(
        password=password, session=session, token=token
    )
