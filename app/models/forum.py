from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship
from app.models.BaseUUID import BaseUUID

if TYPE_CHECKING:
    from app.models.users import ShowUserProfile, Users


class CategoryType(Enum):
    GENERAL = "GENERAL"
    HELP = "HELP"
    TEAM_UP = "TEAM_UP"
    TECHNOLOGY = "TECHNOLOGY"
    HACKATHON = "HACKATHON"
    CP = "CP"


class ForumCreate(SQLModel):
    comment: str = Field(min_length=20)
    parent_comment_id: Optional[UUID] = None
    Category: Optional[CategoryType] = None


class Forum(ForumCreate, BaseUUID, table=True):
    user_id: UUID = Field(foreign_key="users.id")
    likes_count: int = Field(default=0, ge=0)
    dislike_count: int = Field(default=0, ge=0)
    sub_comment: int = Field(default=0, ge=0)
    user: "Users" = Relationship(back_populates="forums")
    forum_reaction: List["Forum_reaction"] = Relationship(back_populates="forums")


class ReadForum(SQLModel):
    comment: str
    parent_comment_id: Optional[UUID]
    Category: Optional[str]
    user_id: UUID
    likes_count: int
    dislike_count: int
    sub_comment: int
    id: UUID
    user: "ShowUserProfile" = Relationship(back_populates="forums")


class Forum_reaction(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    forum_id: UUID = Field(foreign_key="forum.id", primary_key=True)
    reaction: int = Field(ge=0, le=1)
    forums: "Forum" = Relationship(back_populates="forum_reaction")
