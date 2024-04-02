from fastapi import APIRouter

from app.messages import USER_TAG, SKILL_TAG, PASSWORD_TAG

from app.api.v1.endpoints.users import router as user_router
from app.api.v1.endpoints.skills import router as skill_router
from app.api.v1.endpoints.password import router as password_router
from app.core.settings import settings

api = APIRouter(prefix=settings.PROJECT_ENDPOINT_VERSION)

api.include_router(user_router, tags=[USER_TAG])
api.include_router(skill_router, tags=[SKILL_TAG])
api.include_router(password_router, tags=[PASSWORD_TAG])
