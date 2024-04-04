from uuid import UUID
from sqlmodel import select
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import ForumCreate, Forum, Forum_reaction
from app.schema import ReadReactionInput
from sqlalchemy.orm import selectinload


async def add_comment_by_user_id(
        user_id: UUID, forum: ForumCreate, session: AsyncSession
):
    try:
        if forum.parent_comment_id is None and forum.Category is None:
            raise ValueError("Category must be provided for top-level comments")
        if forum.parent_comment_id is not None and forum.Category is not None:
            raise ValueError("Category cannot be provided for sub comments")
        if forum.parent_comment_id:
            statement = select(Forum).where(Forum.id == forum.parent_comment_id)
            parent_comment = (await session.exec(statement)).one_or_none()
            if not parent_comment:
                raise ValueError(
                    f"No comment with id:{str(forum.parent_comment_id)} found"
                )
            parent_comment.sub_comment += 1
            session.add(parent_comment)
            await session.commit()
        # print(forum)
        new_forum = Forum(**jsonable_encoder(forum))
        new_forum.user_id = user_id
        session.add(new_forum)
        await session.commit()
        return "Forum Added"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail=str(e)
        )


async def get_comment_by_comment_id(comment_id: UUID | None, session: AsyncSession):
    try:
        statement = (
            select(Forum)
            .options(selectinload(Forum.user))
            .where(Forum.id == comment_id)
        )
        comment = (await session.exec(statement)).one_or_none()
        if comment is None:
            raise ValueError("No comment found")
        statement = (select(Forum).where(Forum.parent_comment_id == comment.id))
        sub_comment = (await session.exec(statement)).fetchall()
        return {'Parent':comment, "child":sub_comment}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_every_comments_without_id(session: AsyncSession):
    try:
        statement = (
            select(Forum)
            .options(selectinload(Forum.user))
            .where(Forum.parent_comment_id == None)
        )
        comments = (await session.exec(statement)).fetchall()
        if comments is None:
            raise ValueError("No comment found")
        return comments
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_sub_comment_by_comment_id(comment_id: UUID | None, session: AsyncSession):
    try:
        statement = (
            select(Forum)
            .options(selectinload(Forum.user))
            .where(Forum.parent_comment_id == comment_id)
            .limit(5)
        )
        nested_comment = (await session.exec(statement)).fetchall()
        return nested_comment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def patch_react_to_the_comment_by_id(
        vote_state: ReadReactionInput,
        user_id: UUID,
        session: AsyncSession,
        comment_id: UUID,
):
    try:
        statement = select(Forum).where(Forum.id == comment_id)
        comment = (await session.exec(statement)).one_or_none()
        if not comment:
            raise ValueError("No comment in this ID found")
        statement = select(Forum_reaction).where(
            Forum_reaction.forum_id == comment_id and Forum_reaction.user_id == user_id
        )
        comment_reaction = (await session.exec(statement)).one_or_none()
        # Runs when the comment reaction is already exists
        if comment_reaction:
            past_reaction = comment_reaction.reaction
            # If past Reaction is Dislike
            if past_reaction == 0:
                if vote_state.value == "DOWN":
                    pass
                elif vote_state.value == "UP":
                    comment.dislike_count -= 1
                    comment.likes_count += 1
                    comment_reaction.reaction = 1
                    session.add(comment_reaction)
                elif vote_state.value == "NONE":
                    comment.dislike_count -= 1
                    await session.delete(comment_reaction)
                    await session.commit()
                else:
                    raise ValueError("Invalid Reaction")
            # If past Reaction is Like
            elif past_reaction == 1:
                if vote_state.value == "UP":
                    pass
                elif vote_state.value == "DOWN":
                    comment.dislike_count += 1
                    comment.likes_count -= 1
                    comment_reaction.reaction = 0
                    session.add(comment_reaction)
                elif vote_state.value == "NONE":
                    comment.likes_count -= 1
                    await session.delete(comment_reaction)
                    await session.commit()
                else:
                    raise ValueError("Invalid Reaction")
            await session.commit()
        # Runs when the new reaction is added
        else:
            new_reaction = Forum_reaction()
            new_reaction.user_id = user_id
            new_reaction.forum_id = comment_id
            if vote_state.value == "UP":

                comment.likes_count += 1
                new_reaction.reaction = 1
            elif vote_state.value == "DOWN":
                comment.dislike_count += 1
                new_reaction.reaction = 0
            else:
                raise ValueError("Invalid Reaction")
            session.add(new_reaction)
        session.add(comment)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
