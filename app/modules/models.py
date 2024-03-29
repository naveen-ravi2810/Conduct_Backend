from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship, BigInteger, Column

if TYPE_CHECKING:
    pass


# For BaseUUID
class BaseUUID(SQLModel):
    """
    id: int = Field(primary_key=True)
    created_on: datetime = Field(default_factory=datetime.now)
    """

    id: int = Field(primary_key=True)
    created_on: datetime = Field(default_factory=datetime.now)


# User and Skill Link
class UserSkillLink(SQLModel, table=True):
    """
    skill_id: Optional[int] = Field(
        default=None, foreign_key="skill.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    """

    skill_id: Optional[int] = Field(
        default=None, foreign_key="skill.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )


# Login User Details
class LoginUser(SQLModel):
    """
    email: str = Field(regex=r".+@sece\.ac\.in$")
    password: str
    """

    email: str = Field(unique=True, regex="^[a-zA-Z0-9._%+-]+{settings.EMAIL_DOMAIN}$")
    password: str

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
    phone: int = Field(sa_column=Column(BigInteger(), nullable=False, unique=True))
    year: int = Field(ge=2000)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Naveen Ravi",
                "phone": 1234567890,
                "password": "Your_strong_password",
                "email": "naveen.r2021eceb@sece.ac.in",
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
                "otp": 123456,
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
    phone: int
    email: str
    year: int


# Existing Skills Details
class Skill(SQLModel, table=True):
    """
    id: int = Field(primary_key=True)
    skill: str = Field(unique=True, index=True)
    users: List["Users"] = Relationship(
        back_populates="skills", link_model=UserSkillLink
    )
    """

    id: int = Field(primary_key=True)
    skill: str = Field(unique=True, index=True)
    users: List["Users"] = Relationship(
        back_populates="skills", link_model=UserSkillLink
    )


class ReadPeopleBySkill(SQLModel):
    """
    name: str
    year: int
    skills: List[Skill]
    """

    id: int
    name: str
    year: int
    skills: List[Skill]


# Add Skill
class SkillsShow(SQLModel):
    """
    id: int
    skill: str
    """

    id: int
    skill: str


class GetNewSkills(SQLModel):
    """
    Get only skills as a string list\n
    ['Python','C++',]
    """

    skill: List[str]

    class Config:
        json_schema_extra = {
            "example": {"skill": ["Python", "FastAPI", "Flask", "Djangio"]}
        }
