from datetime import datetime
from zlib import crc32

from sqlalchemy.orm import Session
from redis.client import Redis

from models import Url


def get_crc32(text: str) -> str:
    crc = crc32(text.encode())
    return format(crc, 'x')  # 16진수로 변환하여 문자열로 반환


def create_url(db: Session, url_create):
    pre_text = 'abcdefghijklmnopqrstuvwxyz'
    long_url = url_create.long_url
    cnt = 0
    while True:
        short_url = get_crc32(long_url)
        if get_origin_url(db, short_url[:7]):
            long_url += pre_text[cnt % len(pre_text)]
            cnt += 1
            continue
        else:
            break

    db_result = Url(shortUrl=short_url, longUrl=long_url, create_date=datetime.now())
    db.add(db_result)
    db.commit()


def get_shorten_url(db: Session, long_url: str):
    return db.query(Url).filter(Url.longUrl == long_url).first()


def get_origin_url(db: Session, short_url: str):
    return db.query(Url).filter(Url.shortUrl == short_url).first()


def get_url_cache(cache: Redis, short_url: str):
    return cache.get(short_url)


def set_url_cache(cache: Redis, short_url: str, long_url: str):
    cache.set(short_url, long_url)
