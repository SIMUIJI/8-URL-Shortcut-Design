from datetime import datetime

from sqlmodel import Field, SQLModel


class UrlBase(SQLModel):
    short_url: str = Field(index=True)
    long_url: str = Field(index=True)
    is_enable: int = Field(default=1)
    reg_date: datetime = Field(default_factory=datetime.now)


class Url(UrlBase, table=True):
    url_id: int | None = Field(default=None, primary_key=True)


class ResponsePostUrl(UrlBase):
    url_id: int
    short_url: str
