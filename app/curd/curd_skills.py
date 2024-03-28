from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, col, desc, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from typing import List

from app.modules.models import GetNewSkills, Skill, SkillsShow, Users, UserSkillLink


async def get_user_skills_by_user_id(session: AsyncSession, user_id: int):
    try:
        statement = (
            select(Users).options(selectinload(Users.skills)).where(Users.id == user_id)
        )
        result = await session.exec(statement=statement)
        skills = result.one_or_none()
        return skills.skills
    except Exception as e:
        raise HTTPException(status_code=499, detail=f"{e}")


async def get_existing_skills(session: AsyncSession, skill_query: str, page_no: int):
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
        statement = statement.offset((page_no - 1) * 20).limit(40)
        result = await session.exec(statement)
        skills = result.all()
        skills_count = [
            {"id": skill.id, "skill": skill.skill, "count": skill.user_count}
            for skill in skills
        ]
        return skills_count
    except Exception as e:
        raise HTTPException(status_code=400, detail="Unknown error")


# This is only handled by the admin to add the skills
async def add_main_skills(session: AsyncSession, skills: GetNewSkills):
    try:
        for skill in skills:
            statement = select(Skill).where(Skill.skill == skill)
            result = await session.exec(statement=statement)
            out = result.one_or_none()
            if out:
                pass
            else:
                new_skill = Skill(skill=skill)
                session.add(new_skill)
                await session.commit()
        return "Skills added Successfully"
    except Exception as e:
        raise HTTPException(status_code=499, detail=f"{e}")


# Get/Update the Skills of the user
async def add_skill_to_user_by_id(
    user_id: int, skills: List[SkillsShow], session: AsyncSession
):
    try:
        new_skills = []
        for skill in skills:
            statement = select(Skill).where(Skill.skill == skill.skill)
            result = await session.exec(statement=statement)
            skill_obj = result.one_or_none()
            if not skill_obj:
                raise ValueError("Skill Not Found")
            new_skills.append(skill_obj)
        statement = (
            select(Users).options(selectinload(Users.skills)).where(Users.id == user_id)
        )
        result = await session.exec(statement=statement)
        user = result.one_or_none()
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
    page: int,
    count_per_page: int,
    skill: str,
    year: int,
    session: AsyncSession,
    name: str,
    user_id: int,
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
        statement = statement.offset((page - 1) * count_per_page).limit(count_per_page)
        result = await session.exec(statement=statement)
        users = result.all()
        return users
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))


async def get_unadded_skills(
    session: AsyncSession, user_id: int, skill: str, page_no: int
):
    try:
        subquery = (
            select(UserSkillLink.skill_id)
            .join(Users)
            .where(Users.id == user_id)
            .as_scalar()
        )
        statement = (
            select(Skill)
            .where(Skill.id.notin_(subquery))
            .where(col(Skill.skill).ilike("%" + skill + "%" if skill else "%"))
            .offset((page_no - 1) * 20)
            .limit(20)
        )
        result = await session.exec(statement=statement)
        return result.all()
    except Exception as e:
        raise HTTPException(status_code=499, detail=f"{e}")
