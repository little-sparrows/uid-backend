from datetime import datetime

from pydantic import BaseModel


class CreateUser(BaseModel):
    fingerprint_id: str
    created_at: datetime
    deleted_at: datetime


class User(BaseModel):
    id: int
    fingerprint_id: str
    created_at: datetime
    deleted_at: datetime
