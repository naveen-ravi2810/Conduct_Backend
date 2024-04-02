from fastapi import APIRouter, Depends, status, UploadFile, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import UserCreate, UserURIUpdate, LoginUser, ShowUserProfile
from app.schema import (
    BaseStatusResponse,
    LoginResponseSchema,
    TokenResponse,
    TokenDetailsResponse,
)
from app.core.settings import settings
from app.core.db import get_session, r_conn
from app.core.security import get_user_credentials
from app.curd.user import (
    create_user,
    send_otp_to_email_for_register,
    update_user,
    login_user,
    show_user_profile,
    logout_user,
)


router = APIRouter()


# To get the users data
@router.get(
    "/profile/{user_id}", status_code=status.HTTP_200_OK, response_model=ShowUserProfile
)
async def get_user_by_id(
    user_id: str,
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    user = await show_user_profile(user_id=user_id, session=session)
    if user.id != token_details.id:
        user.phone = user.phone[0:5] + "*****"
    user.__dict__.update({"curr_user": user.id == token_details.id})
    return user


# Sending profile uri for edit and hiding other informations
@router.get("/update_uri", status_code=status.HTTP_200_OK, response_model=UserURIUpdate)
async def get_user_updates_uri_by_id(
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return await show_user_profile(user_id=token_details.id, session=session)


# Get the users cedentials and return the valid token
@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginResponseSchema
)
async def login_user_by_credentials(
    user_details: LoginUser, session: AsyncSession = Depends(get_session)
):
    return LoginResponseSchema(
        access_token=await login_user(
            user_details=user_details, session=session, r_conn=r_conn
        )
    )


# Once the user logout the token is removed from redis for the token secure purpose
@router.delete(
    "/logout", status_code=status.HTTP_200_OK, response_model=BaseStatusResponse
)
async def logout_user_by_token(
    token_details: TokenResponse = Depends(get_user_credentials),
):
    return BaseStatusResponse(
        message=await logout_user(user_id=token_details.id, r_conn=r_conn)
    )


# Add new user to the Application
@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=BaseStatusResponse
)
async def create_new_user(
    user_details: UserCreate, session: AsyncSession = Depends(get_session)
):
    return BaseStatusResponse(
        message=await create_user(
            user_details=user_details, session=session, r_conn=r_conn
        )
    )


# Update the Uri's and description
@router.put(
    "/update_user", status_code=status.HTTP_202_ACCEPTED, response_model=UserURIUpdate
)
async def update_user_by_id(
    user_details: UserURIUpdate,
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return await update_user(
        user_id=token_details.id, user_details=user_details, session=session
    )


# To add the profile picture and store in s3 bucket
# ?????????????????????????????????????????????????????????????????????????
@router.patch(
    "/profile_picture",
    status_code=status.HTTP_200_OK,
    response_model=BaseStatusResponse,
)
def update_profile_picture(
    file: UploadFile,
    # token_details: TokenResponse = Depends(get_user_credentials),
    # session: AsyncSession = Depends(get_session),
):
    return BaseStatusResponse(message=file.filename)


# To validate the Token
@router.get("/token", status_code=200, response_model=TokenDetailsResponse)
async def check_token_validation(
    token_details: TokenResponse = Depends(get_user_credentials),
):
    return TokenDetailsResponse(
        message="Token Validated",
        email=token_details.email,
        id=token_details.id,
    )


# Sends a validated otp before getting the user to the application
@router.get("/email_verification", status_code=200)
async def send_verification_to_email(
    email: str, session: AsyncSession = Depends(get_session)
):
    if not email.endswith(settings.EMAIL_DOMAIN):
        raise HTTPException(
            status_code=400, detail=f"Email must end with {settings.EMAIL_DOMAIN}"
        )
    return await send_otp_to_email_for_register(
        email=email, session=session, r_conn=r_conn
    )
