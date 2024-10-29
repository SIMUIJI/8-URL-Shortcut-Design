import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from api import url_router
from db import create_db_and_tables

app: FastAPI = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


def create_app(_app) -> FastAPI:
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=("GET", "POST", "PUT", "DELETE"),
        allow_headers=["*"],
    )

    _app.include_router(url_router, prefix="/api/v1")

    def game_credit_openapi():
        if _app.openapi_schema:
            return _app.openapi_schema
        openapi_schema = get_openapi(
            title="url-shortener",
            version="1.0",
            routes=_app.routes,
        )
        _app.openapi_schema = openapi_schema
        return _app.openapi_schema

    _app.openapi = game_credit_openapi

    return _app


app = create_app(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5959, reload=True, access_log=False)
