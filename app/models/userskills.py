from uuid import UUID

from sqlmodel import SQLModel, Field


class UserSkillLink(SQLModel, table=True):
    """
    skill_id: Optional[int] = Field(
        default=None, foreign_key="skill.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    """

    skill_id: int = Field(foreign_key="skill.id", primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
