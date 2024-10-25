import os
from typing import Annotated, AsyncIterator

from dotenv import load_dotenv
from fastapi import Depends
from redis import asyncio as aioredis

load_dotenv()


async def init_redis_pool() -> AsyncIterator[aioredis.Redis]:
    session = await aioredis.from_url(
        f"redis://{os.environ.get('REDIS_SERVER')}",
        port=os.environ.get("REDIS_PORT"),
        password=os.environ.get("REDIS_PASSWORD"),
        encoding="utf-8",
        decode_responses=True,
    )
    yield session
    await session.close()


SessionRedis = Annotated[AsyncIterator[aioredis.Redis], Depends(init_redis_pool)]
