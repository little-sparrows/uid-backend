from datetime import datetime
from pydantic import BaseModel
from pydantic.validators import parse_datetime


class TimezoneIndependentDatetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime
        yield cls.normalize_tz

    @classmethod
    def normalize_tz(cls, v: datetime):
        if not v.utcoffset():
            return v
        else:
            return (v - v.utcoffset()).replace(tzinfo=None)


class NoContentResponse(BaseModel):
    message: str
