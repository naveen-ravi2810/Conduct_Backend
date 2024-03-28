from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.modules.schema import ResponseSchema, TokenResponse
from app.core.db import get_session
from app.core.security import get_user_credentials
from app.modules.models import ReadPeopleBySkill, SkillsShow
from app.curd.curd_skills import (
    get_existing_skills,
    add_skill_to_user_by_id,
    get_user_details_by_name_skill_year,
    get_user_skills_by_user_id,
    get_unadded_skills,
)

router = APIRouter()


# Return Skills For the Edit purpose of the current user
@router.get("/get_user_skills", status_code=status.HTTP_200_OK)
async def get_user_skills(
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return await get_user_skills_by_user_id(session=session, user_id=token_details.id)


# Update new skills of the user
@router.put(
    "/update_skill", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema
)
async def add_skill_to_user(
    skills: List[SkillsShow],
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return ResponseSchema(
        message=await add_skill_to_user_by_id(
            user_id=token_details.id, skills=skills, session=session
        )
    )


# Display every skills and the count of users having it
@router.get("/get_skills", status_code=status.HTTP_201_CREATED)
async def get_skills_by_query(
    page_no: int | None = 1,
    skill: str | None = None,
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return await get_existing_skills(
        session=session, skill_query=skill, page_no=page_no
    )


# Displays the unadded skills of the current user
@router.get("/get_unadded_skills", status_code=status.HTTP_200_OK)
async def get_unadded_skills_by_query(
    page_no: int | None = 1,
    skill: str | None = None,
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return await get_unadded_skills(
        session=session, skill=skill, user_id=token_details.id, page_no=page_no
    )


# Display the user minimal details by the filter of skills, name, year of passing
@router.get(
    "/get_user_by_filter",
    status_code=status.HTTP_200_OK,
    response_model=List[ReadPeopleBySkill] | None,
)
async def get_user_by_filter(
    page: int | None = 1,
    count_per_page: int | None = 10,
    skill: str | None = None,
    name: str | None = None,
    year: int | None = None,
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return await get_user_details_by_name_skill_year(
        page=page,
        count_per_page=count_per_page,
        skill=skill,
        year=year,
        name=name,
        session=session,
        user_id=token_details.id,
    )
