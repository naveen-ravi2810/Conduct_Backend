from enum import Enum
from typing import Optional, List
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship
from app.models.BaseUUID import BaseUUID


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


class Forum_reaction(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    forum_id: UUID = Field(foreign_key="forum.id", primary_key=True)
    reaction: int = Field(ge=0, le=1)
