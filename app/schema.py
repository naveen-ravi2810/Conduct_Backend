"""
Data validations like
- BaseStatusResponse
- LoginResponseSchema
- TokenResponse
- TokenDetailsResponse
- ChangePasswordSchema
- NewPasswordSchema
"""

from pydantic import BaseModel


class BaseStatusResponse(BaseModel):
    """
    status: bool = True
    message: str
    """

    status: str = "ok"
    message: str | None = None


class LoginResponseSchema(BaseModel):
    """
    status: bool = True
    access_token: str
    """

    status: bool = True
    access_token: str


class TokenResponse(BaseModel):
    """
    id: str
    email: str
    """

    id: str
    email: str


class TokenDetailsResponse(BaseModel):
    """
    id: str
    email: str
    status: bool = True
    message: str
    """

    id: str
    email: str
    status: bool = True
    message: str


class ChangePasswordSchema(BaseModel):
    """
    old_password: str
    new_password: str
    re_enter_new_password: str
    """

    old_password: str
    new_password: str
    re_enter_new_password: str


class NewPasswordSchema(BaseModel):
    """
    otp: str
    new_password: str
    re_enter_new_password: str
    """

    otp: str
    new_password: str
    re_enter_new_password: str
