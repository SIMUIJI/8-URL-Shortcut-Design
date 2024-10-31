from starlette.middleware.cors import CORSMiddleware

from config import settings
from domain.url import url_router
from fastapi import FastAPI

app = FastAPI(
    title=settings.PROJECT_NAME,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(url_router.router)

"""
FastAPI 실행 명령어
uvicorn main:app  --host 192.168.184.1 --reload
"""
