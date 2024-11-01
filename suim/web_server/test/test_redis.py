import redis
from config import settings


def test_get_cache():
    cache = redis.Redis.from_url(url=settings.CACHE_URI)
    try:
        yield cache
    finally:
        cache.close()


def test_main():
    r = redis.Redis.from_url(url="redis://default:password@localhost:6379/0")
    print(r.ping())
    rs = r.get("c45fefb4")
    if not rs:
        r.set("c45fefb4", "https://docs.pydantic.dev/2.9/errors/usage_errors/#custom-json-schema")
    rs = r.get("c45fefb4")
    print()
