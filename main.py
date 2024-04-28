"""
Main file to run application
"""

import time
import logging
import asyncio
from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

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


add_pagination(app)
disable_installed_extensions_check()


logging.basicConfig(
    filename="requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@app.middleware("http")
async def add_log(request: Request, call_next):
    """
    middleware to create log files
    """
    request_method = request.method
    request_url = request.url.path
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time
    logging.info(
        "Request: %s %s, Response Time: %s", request_method, request_url, response_time
    )
    response.headers["X-Time-Elapsed"] = str(response_time)[:6]
    return response


app.include_router(api)


@app.get("/health")
async def health_check():
    return {"status": True}


if __name__ == "__main__":
    asyncio.run(init_db_fun())
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
