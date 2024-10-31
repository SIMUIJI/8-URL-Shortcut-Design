from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

import redis

# from aioredis import from_url

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

naming_convention = {
    "ix": "ix_%(column_0_label)s",  # index key
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # unique key
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # foreign key
    "pk": "pk_%(table_name)s",  # primary key
}
Base.metadata = MetaData(naming_convention=naming_convention)


def get_db():
    """DB 세션 객체를 리턴하는 제너레이터 함수"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cache():
    cache = redis.Redis.from_url(url=settings.CACHE_URI, decode_responses=True)
    try:
        yield cache
    finally:
        cache.close()
