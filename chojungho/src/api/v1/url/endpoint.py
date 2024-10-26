import json

import base62
from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from sqlmodel import select

from db import SessionDep, SessionRedis, UrlTable

from .model import RequstPostUrl, ResponsePostUrl

router = APIRouter(prefix="/url", tags=["URL"])


@router.get("/")
async def get_url(short_url: str, rdb_session: SessionDep, redis_session: SessionRedis):
    if url_cache_info := await redis_session.get(f"{short_url}"):
        url_cache_info = json.loads(url_cache_info)
        return RedirectResponse(url_cache_info["long_url"], status_code=302)
    else:
        try:
            long_url = rdb_session.exec(select(UrlTable).where(UrlTable.short_url == short_url)).first().long_url
            cache_data: str = json.dumps({"long_url": long_url, "ex": 604800})
            await redis_session.set(name=f"{short_url}", value=cache_data, ex=604800)
            return RedirectResponse(long_url, status_code=302)
        except AttributeError:
            return JSONResponse(content={"message": "URL이 존재하지 않습니다."}, status_code=404)
        except Exception as e:
            return JSONResponse(content={"message": f"Server Error\n{e}"}, status_code=500)


@router.post("/", response_model=ResponsePostUrl)
async def post_url(url_info: RequstPostUrl, rdb_session: SessionDep, redis_session: SessionRedis):
    try:
        short_url = rdb_session.exec(select(UrlTable).where(UrlTable.long_url == url_info.long_url)).first().short_url
        return JSONResponse(content={"message": f"이미 존재하는 URL입니다.\n단축URL : {short_url}"}, status_code=200)
    except AttributeError:
        redis_unq_id = await redis_session.incr("url_shortener_id")
        short_url = base62.encode(redis_unq_id)
        rdb_session.add(UrlTable(url_id=redis_unq_id, short_url=short_url, long_url=url_info.long_url))
        await redis_session.set(f"{short_url}", json.dumps({"long_url": url_info.long_url, "ex": 604800}), ex=604800)
        return JSONResponse(content={"message": f"등록되었습니다.\n단축URL : {short_url}"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Server Error\n{e}"}, status_code=500)
