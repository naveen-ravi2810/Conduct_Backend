'''
Main file to run application
'''
import logging
from fastapi import FastAPI

from app.api.v1.api import api
from app.core.settings import settings

from app.core.init_db import init_db_fun


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    contact={
        "name": settings.PROJECT_OWNER_NAME,
        "url": settings.PROJECT_OWNER_URL,
        "email": settings.PROJECT_OWNER_EMAIL,
    },
)


app.include_router(api)

if __name__ == "__main__":
    import uvicorn
    import asyncio

    asyncio.run(init_db_fun())
    logging.info("application started successfully")
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
