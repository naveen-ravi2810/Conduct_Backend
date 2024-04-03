from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class BaseUUID(SQLModel):
    """
    id: int = Field(primary_key=True)
    created_on: datetime = Field(default_factory=datetime.now)
    """

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now()}
    )
