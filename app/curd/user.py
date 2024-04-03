from uuid import uuid4, UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select  # pylint: disable=C0412
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from app.celery_worker import send_otp
from app import messages
from app.models import UserCreate, Users, UserURIUpdate, LoginUser, Forum
from app.core.security import hash_password, check_password, create_access_token
from app.core.settings import settings


async def login_user(user_details: LoginUser, session: AsyncSession, r_conn: Redis):
    try:
        statement = select(Users).where(Users.email == user_details.email)
        user = (await session.exec(statement=statement)).one_or_none()
        if user:
            if check_password(user_details.password, user.password):
                token = await create_access_token(id=user.id, email=user.email)
                await r_conn.setex(
                    name=f"access_token:{user.id}",
                    value=token,
                    time=settings.JWT_EXPIRE_TIME_IN_SEC,
                )
                return token

            raise ValueError("Invalid Username/ Password")

        raise ValueError("Invalid Username/ Password")
    except Exception as e:
        # print("e")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")


async def logout_user(user_id: UUID, r_conn: Redis):
    try:
        await r_conn.delete(f"access_token:{user_id}")
        return "User Logout Successfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


async def create_user(user_details: UserCreate, session: AsyncSession, r_conn: Redis):
    try:
        encoded_otp = await r_conn.get(f"register_otp:{user_details.email}")
        if encoded_otp and encoded_otp.decode("utf-8") == str(user_details.otp):
            encoded_users = jsonable_encoder(user_details, exclude={"otp"})
            user = Users(**encoded_users)
            user.password = hash_password(password=user_details.password)
            session.add(user)
            await session.commit()
            await r_conn.delete(f"register_otp:{user_details.email}")
            return messages.USER_CREATED_MESSAGE
        raise ValueError("Invalid OTP")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e}")


async def update_user(
    user_id: UUID, user_details: UserURIUpdate, session: AsyncSession
):
    try:
        user = await session.get(Users, user_id)
        user_data = user_details.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.USER_CANNOT_UPDATED_SUCCESSFULLY,
        )


async def show_user_profile(user_id: UUID, session: AsyncSession):
    try:
        statement = (
            select(Users)
            .options(selectinload(Users.forums))
            .options(selectinload(Users.skills))
            .where(Users.id == user_id)
        )
        user = (await session.exec(statement)).one_or_none()
        if user:
            return user
        raise ValueError("User Not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def send_otp_to_email_for_register(
    email: str, session: AsyncSession, r_conn: Redis
):
    try:
        statement = select(Users).where(Users.email == email)
        user = (await session.exec(statement=statement)).one_or_none()
        if user:
            raise ValueError("User Already Exists")
        otp = str(uuid4().int)[-6:]
        send_otp.delay(email=email, otp=otp)
        await r_conn.setex(name=f"register_otp:{email}", value=otp, time=600)
        return "OTP Send Sucessfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
