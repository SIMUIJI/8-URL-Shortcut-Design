import json

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from sqlmodel import select

from db import SessionDep, SessionRedis, UrlTable

router = APIRouter(prefix="/url", tags=["URL"])


@router.get("/", response_model=None)
async def get_url(short_url: str, rdb_session: SessionDep, rdis_session: SessionRedis) -> RedirectResponse | str:
    if url_cache_info := await rdis_session.get(f"{short_url}"):
        url_cache_info = json.loads(url_cache_info)
        return RedirectResponse(url_cache_info["long_url"])
    elif long_url := rdb_session.exec(select(UrlTable).where(UrlTable.short_url == short_url)).first().long_url:
        try:
            cache_data: str = json.dumps({"long_url": long_url, "ex": 604800})
            await rdis_session.set(name=f"{short_url}", value=cache_data, ex=604800)
            return RedirectResponse(long_url)
        except Exception as e:
            return str(e)
    else:
        return "Not Found"
