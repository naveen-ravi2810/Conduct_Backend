import os
from pydantic_settings import BaseSettings
from pydantic import HttpUrl
from dotenv import load_dotenv

from app import messages

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = messages.PROJECT_NAME
    PROJECT_DESCRIPTION: str = messages.PROJECT_DESRIPTION
    PROJECT_VERSION: str = messages.PROJECT_VERSION
    PROJECT_OWNER_URL: HttpUrl = messages.PROJECT_OWNER_URL
    PROJECT_OWNER_NAME: str = messages.PROJECT_OWNER_NAME
    PROJECT_OWNER_EMAIL: str = messages.PROJECT_OWNER_EMAIL

    EMAIL_DOMAIN: str = os.environ.get("DOMAIN_EMAIL")

    EMAIL_SENDER_ID: str = os.environ.get("EMAIL_EMAIL")
    EMAIL_SENDER_PASSWORD: str = os.environ.get("EMAIL_PASSWORD")

    CELERY_BACKEND: str = os.environ.get("CELERY_BACKEND")
    CELERY_BROKER: str = os.environ.get("CELERY_BROKER")

    PROJECT_ENDPOINT_VERSION: str = "/api/v1"

    DB_URI: str = os.environ.get("POSTGRESQL_URI")

    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_USERNAME: str = os.environ.get("REDIS_USER_NAME")
    REDIS_PASSWORD: str = os.environ.get("REDIS_PASSWORD")
    REDIS_PORT: int = os.environ.get("REDIS_PORT")
    REDIS_DB: int = os.environ.get("REDIS_DB")

    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM")
    JWT_EXPIRE_TIME_IN_SEC: int = os.environ.get("JWT_EXPIRE_IN_SEC")


settings = Settings()
