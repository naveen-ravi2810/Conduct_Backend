from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

from app.modules import messages

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = messages.PROJECT_NAME
    PROJECT_DESCRIPTION: str = messages.PROJECT_DESRIPTION
    PROJECT_VERSION: str = messages.PROJECT_VERSION
    PROJECT_OWNER_URL: str = messages.PROJECT_OWNER_URL
    PROJECT_OWNER_NAME: str = messages.PROJECT_OWNER_NAME
    PROJECT_OWNER_EMAIL: str = messages.PROJECT_OWNER_EMAIL

    EMAIL_DOMAIN: str = os.environ.get("domain_email")

    EMAIL_SENDER_ID: str = os.environ.get("email_email")
    EMAIL_SENDER_PASSWORD: str = os.environ.get("email_password")

    CELERY_BACKEND: str = os.environ.get("celery_backend")
    CELERY_BROKER: str = os.environ.get("celery_broker")

    PROJECT_ENDPOINT_VERSION: str = "/api/v1"

    DB_URI: str = os.environ.get("postgresql_uri")

    REDIS_HOST: str = os.environ.get("redis_host")
    REDIS_USERNAME: str = os.environ.get("redis_user_name")
    REDIS_PASSWORD: str = os.environ.get("redis_password")
    REDIS_PORT: int = os.environ.get("redis_port")
    REDIS_DB: int = os.environ.get("redis_db")

    JWT_SECERT_KEY: str = os.environ.get("jwt_secret_key")
    JWT_ALGORITHM: str = os.environ.get("jwt_algorithm")
    JWT_EXPIRE_TIME_IN_SEC: int = os.environ.get("jwt_expire_in_sec")


settings = Settings()
