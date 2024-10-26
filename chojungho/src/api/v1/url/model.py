from pydantic import BaseModel


class RequstPostUrl(BaseModel):
    long_url: str


class ResponsePostUrl(BaseModel):
    message: str
