"""
Data validations like
- ResponseSchema
- LoginResponseSchema
- TokenResponse
- TokenDetailsResponse
- ChangePasswordSchema
- NewPasswordSchema
"""

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    """
    status: bool = True
    message: str
    """

    status: bool = True
    message: str


class LoginResponseSchema(BaseModel):
    """
    status: bool = True
    access_token: str
    """

    status: bool = True
    access_token: str


class TokenResponse(BaseModel):
    """
    id: int
    email: str
    """

    id: int
    email: str


class TokenDetailsResponse(BaseModel):
    """
    id: int
    email: str
    status: bool = True
    message: str
    """

    id: int
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
