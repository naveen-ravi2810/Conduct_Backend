from datetime import timedelta, datetime
from typing import Annotated
from uuid import UUID

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import bcrypt
from pytz import timezone
from fastapi import Depends, HTTPException  # pylint: disable=C0412

from app.core.db import r_conn
from app.core.settings import settings
from app.schema import TokenResponse


def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password.encode()
    )


async def create_access_token(id: UUID, email: str):
    ist = timezone("Asia/Kolkata")
    iat = datetime.now(ist)
    exp = iat + timedelta(seconds=settings.JWT_EXPIRE_TIME_IN_SEC)
    return jwt.encode(
        {"sub": str(id), "email": email, "exp": exp, "iat": iat},
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
    )


async def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return payload
    except:
        return None


auth_schema = HTTPBearer()


async def get_user_credentials(
    token: HTTPAuthorizationCredentials = Depends(auth_schema),
) -> TokenResponse:
    """
    Return only the ID of the user by the token
    """
    try:
        data = await decode_token(token.credentials)
        if not data:
            raise ValueError("Invalid Token")
        r_token = await r_conn.get(name=f"access_token:{data['sub']}")
        if r_token:
            exist_token = r_token.decode("utf-8")
            if exist_token == token.credentials:
                return TokenResponse(email=data["email"], id=UUID(data["sub"]))
            raise ValueError("Old/ Invalid Token")
        raise ValueError("Expired Token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"{e}")
