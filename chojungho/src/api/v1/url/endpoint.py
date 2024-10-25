import json

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from sqlmodel import select

from db import ResponsePostUrl, SessionDep, SessionRedis, UrlTable

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


@router.post("/", response_model=ResponsePostUrl)
async def post_url(long_url: str, rdb_session: SessionDep) -> ResponsePostUrl:
    # 1. long_url이 있는지 없는지 체크하고 있으면 반환
    # 2. 없으면 새로운 short_url을 생성하고 DB및 Redis에 저장하고 short_url을 반환
    ...
