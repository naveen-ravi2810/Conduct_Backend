from typing import Optional, List
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship
from app.models.BaseUUID import BaseUUID
from app.models.userskills import UserSkillLink
from app.models.skills import Skill
from app.models.forum import Forum


# Login User Details
class LoginUser(SQLModel):
    """
    email: str = Field(regex=r".+@sece\.ac\.in$")
    password: str
    """

    email: str = Field(unique=True, regex="^[a-zA-Z0-9._%+-]+{settings.EMAIL_DOMAIN}$")
    password: str = Field(min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "teststudent@sece.ac.in",
                "password": "teststudent",
            }
        }


# Users Details
class UserBasicCreate(LoginUser):
    """
    email: str = Field(regex=r".+@sece\.ac\.in$")
    password: str
    name: str = Field(index=True, min_length=5)
    phone: int = Field(sa_column=Column(BigInteger(), nullable=False, unique=True))
    year: int = Field(ge=2000)
    """

    name: str = Field(index=True, min_length=5)
    phone: str = Field(unique=True)
    year: int = Field(ge=1900)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Naveen Ravi",
                "phone": 1234567890,
                "password": "Your_strong_password",
                "email": "naveen.r2021eceb@sece.ac.in",
                "year": 2025,
            }
        }


class UserCreate(UserBasicCreate):
    otp: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Naveen Ravi",
                "phone": 1234567890,
                "password": "Your_strong_password",
                "email": "naveen.r2021eceb@sece.ac.in",
                "year": "2025",
                "otp": "123456",
            }
        }


# Users Table
class Users(BaseUUID, UserBasicCreate, table=True):
    """
    id: int = Field(primary_key=True)
    created_on: datetime = Field(default_factory=datetime.now)
    name: str = Field(index=True, min_length=5)
    phone: int = Field(sa_column=Column(BigInteger(), nullable=False, unique=True))
    year: int = Field(ge=2000)
    github_uri: Optional[str] = Field(default=None)
    linkedin_uri: Optional[str] = Field(default=None)
    leetcode_uri: Optional[str] = Field(default=None)
    codechef_uri: Optional[str] = Field(default=None)
    portfolio_uri: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    skills: List["Skill"] = Relationship(
        back_populates="users", link_model=UserSkillLink
    )
    forums: List["Forum"] = Relationship(back_populates="user")
    """

    github_uri: Optional[str] = Field(default=None)
    linkedin_uri: Optional[str] = Field(default=None)
    leetcode_uri: Optional[str] = Field(default=None)
    codechef_uri: Optional[str] = Field(default=None)
    portfolio_uri: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    skills: List["Skill"] = Relationship(
        back_populates="users", link_model=UserSkillLink
    )
    forums: List["Forum"] = Relationship(back_populates="user")


# Update user Details
class UserURIUpdate(SQLModel):
    """
    github_uri: Optional[str] = None
    linkedin_uri: Optional[str] = None
    leetcode_uri: Optional[str] = None
    codechef_uri: Optional[str] = None
    portfolio_uri: Optional[str] = None
    description: Optional[str] = None
    """

    github_uri: Optional[str] = None
    linkedin_uri: Optional[str] = None
    leetcode_uri: Optional[str] = None
    codechef_uri: Optional[str] = None
    portfolio_uri: Optional[str] = None
    description: Optional[str] = None


# Users Profile Details
class ShowUserProfile(BaseUUID, UserURIUpdate):
    """
    id: int = Field(primary_key=True)
    created_on: datetime = Field(default_factory=datetime.now)
    skills: List["Skill"]
    name: str
    phone: int
    email: str
    year : int
    curr_user: bool
    name: str
    phone: int
    email: str
    year: int

    """

    curr_user: bool
    skills: List["Skill"]
    name: str
    phone: str
    email: str
    year: int
    forums: List["Forum"]


class ReadPeopleBySkill(SQLModel):
    """
    name: str
    year: int
    skills: List[Skill]
    """

    id: UUID
    name: str
    year: int
    skills: List["Skill"]
