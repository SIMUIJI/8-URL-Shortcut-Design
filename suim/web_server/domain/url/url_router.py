from sqlalchemy.orm import Session
from redis.client import Redis
from fastapi.responses import RedirectResponse

from database import get_db, get_cache
from domain.url import url_crud, url_schema
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/v1",
)


@router.post("/data/shorten", response_model=url_schema.UrlResult)
def create_shorten_url(
        _url_create: url_schema.UrlCreate,
        db: Session = Depends(get_db),
):
    url = url_crud.get_shorten_url(db, long_url=_url_create.long_url)
    if not url:
        url_crud.create_url(db, url_create=_url_create)
        url = url_crud.get_shorten_url(db, long_url=_url_create.long_url)
    # return {'shortUrl': f'http://192.168.184.1:8000/api/v1/shortUrl/{url.shortUrl}'}
    return {'shortUrl': f'http://192.168.184.1/api/v1/shortUrl/{url.shortUrl}'}


@router.get("/shortUrl/{short_url}")
def url_origin(short_url: str, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    long_url = url_crud.get_url_cache(cache=cache, short_url=short_url)
    if not long_url:
        result = url_crud.get_origin_url(db=db, short_url=short_url)
        long_url = result.longUrl
        url_crud.set_url_cache(cache=cache, short_url=short_url, long_url=long_url)
    return RedirectResponse(long_url)
