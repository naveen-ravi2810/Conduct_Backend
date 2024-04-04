from uuid import UUID
from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.forum import ForumCreate, Forum
from app.schema import TokenResponse
from app.core.security import get_user_credentials
from app.core.db import get_session
from app.schema import ReadReactionInput
from app.curd.forum import (
    add_comment_by_user_id,
    get_comment_by_comment_id,
    get_sub_comment_by_comment_id,
    get_every_comments_without_id,
    patch_react_to_the_comment_by_id,
)

router = APIRouter()


@router.post("/comment", status_code=status.HTTP_201_CREATED)
async def add_comment(
    forum: ForumCreate,
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return await add_comment_by_user_id(
        user_id=token_details.id, forum=forum, session=session
    )


@router.get(
    "/comment",
    dependencies=[Depends(get_user_credentials)],
    status_code=status.HTTP_200_OK,
)
async def get_comment(
    comment_id: UUID | None = None, session: AsyncSession = Depends(get_session)
):
    return await get_comment_by_comment_id(
        comment_id=comment_id,
        session=session,
    )


@router.get(
    "/comments",
    dependencies=[Depends(get_user_credentials)],
    status_code=status.HTTP_200_OK,
)
async def get_every_comments(
    session: AsyncSession = Depends(get_session),
) -> Page[Forum]:
    return paginate(await get_every_comments_without_id(session=session))


@router.get(
    "/sub_comment",
    dependencies=[Depends(get_user_credentials)],
    status_code=status.HTTP_200_OK,
)
async def get_comment(
    comment_id: UUID | None = None, session: AsyncSession = Depends(get_session)
) -> Page[Forum]:
    return paginate(
        await get_sub_comment_by_comment_id(
            comment_id=comment_id,
            session=session,
        )
    )


@router.patch("/comment_reaction")
async def like_comment_by_id(
    vote_state: ReadReactionInput,
    comment_id: UUID,
    token_details: TokenResponse = Depends(get_user_credentials),
    session: AsyncSession = Depends(get_session),
):
    return await patch_react_to_the_comment_by_id(
        vote_state=vote_state,
        comment_id=comment_id,
        session=session,
        user_id=token_details.id,
    )
