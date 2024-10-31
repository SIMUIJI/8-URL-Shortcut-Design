import datetime

from pydantic import BaseModel, field_validator


class UrlCreate(BaseModel):
    long_url: str

    # 빈 문자열을 허용하지 않기 위한 함수
    @field_validator("long_url")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


class Url(BaseModel):
    id: int
    url: str
    shortUrl: str
    longUrl: str
    create_date: datetime.datetime | None = None


class UrlResult(BaseModel):
    shortUrl: str


class UrlRedirect(BaseModel):
    longUrl: str
