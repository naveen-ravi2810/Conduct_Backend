from typing import List
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, col, desc, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models import GetNewSkills, Skill, SkillsShow, Users, UserSkillLink


async def get_user_skills_by_user_id(session: AsyncSession, user_id: UUID):
    try:
        statement = (
            select(Users).options(selectinload(Users.skills)).where(Users.id == user_id)
        )
        skills = (await session.exec(statement=statement)).one_or_none()
        return skills.skills
    except Exception as e:
        raise HTTPException(status_code=499, detail=f"{e}")


async def get_existing_skills(session: AsyncSession, skill_query: str):
    try:
        statement = select(
            Skill.id,
            Skill.skill,
            func.count(UserSkillLink.user_id).label("user_count"),
        ).outerjoin(UserSkillLink)
        if skill_query:
            statement = statement.filter(Skill.skill.ilike(f"%{skill_query}%"))
        statement = statement.group_by(Skill.id, Skill.skill).order_by(
            desc("user_count")
        )
        skills = (await session.exec(statement)).all()
        skills_count = [
            {"id": skill.id, "skill": skill.skill, "count": skill.user_count}
            for skill in skills
        ]
        return skills_count
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
        

# Get/Update the Skills of the user
async def add_skill_to_user_by_id(
    user_id: str, skills: List[SkillsShow], session: AsyncSession
):
    try:
        new_skills = []
        for skill in skills:
            statement = select(Skill).where(Skill.skill == skill.skill)
            skill_obj = (await session.exec(statement=statement)).one_or_none()
            if not skill_obj:
                raise ValueError("Skill Not Found")
            new_skills.append(skill_obj)
        statement = (
            select(Users).options(selectinload(Users.skills)).where(Users.id == user_id)
        )
        user = (await session.exec(statement=statement)).one_or_none()
        if not user:
            raise ValueError("User Not Found")
        user.skills = new_skills
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return "User Skill Updated Successfully"
    except Exception as e:
        raise HTTPException(status_code=499, detail=f"{str(e)}")


async def get_user_details_by_name_skill_year(
    skill: str,
    year: int,
    session: AsyncSession,
    name: str,
    user_id: UUID,
):
    try:
        statement = (
            select(Users).options(selectinload(Users.skills)).where(Users.id != user_id)
        )
        if name:
            statement = statement.where(col(Users.name).ilike("%" + name + "%"))
        if year:
            statement = statement.filter(Users.year == year)
        if skill:
            statement = statement.where(
                Users.skills.any(Skill.skill.ilike("%" + skill + "%"))
            )
        users = (await session.exec(statement=statement)).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))


async def get_unadded_skills(session: AsyncSession, user_id: UUID, skill: str):
    try:
        subquery = (
            select(UserSkillLink.skill_id)
            .join(Users)
            .where(Users.id == user_id)
            .scalar_subquery()
        )
        statement = (
            select(Skill)
            .where(Skill.id.notin_(subquery))
            .where(col(Skill.skill).ilike("%" + skill + "%" if skill else "%"))
        )
        result = (await session.exec(statement=statement)).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
