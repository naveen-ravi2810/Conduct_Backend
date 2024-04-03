from typing import List

from sqlmodel import SQLModel, Field, Relationship

from app.models.userskills import UserSkillLink


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


# Existing Skills Details
class SkillsShow(SQLModel):
    """
    id: int
    skill: str
    """

    id: int
    skill: str


# Add Skill


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
