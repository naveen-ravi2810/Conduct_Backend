"""
Main file to run application
"""
import time
from fastapi import FastAPI, Request

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


@app.middleware("http")
async def add_log(request: Request, call_next):
    request_method = request.method
    request_url = request.url.path
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time
    with open("log.txt", mode="a") as log_file:
        content = f"Path: {request_url} , Method: {request_method} , Response_time: {response_time}\n"
        log_file.write(content)
    response.headers["X-Time-Elapsed"] = str(response_time)[:6]
    return response


app.include_router(api)

if __name__ == "__main__":
    import uvicorn
    import asyncio

    asyncio.run(init_db_fun())
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
