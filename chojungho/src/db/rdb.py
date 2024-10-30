import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

pg_engine = create_engine(
    f"postgresql://{os.environ.get('PGPOOL_USER')}:"
    f"{os.environ.get('PGPOOL_PASSWORD')}@"
    f"{os.environ.get('PGPOOL_HOST')}:"
    f"{os.environ.get('PGPOOL_PORT')}/"
    f"{os.environ.get('PGPOOL_NAME')}"
)


async def create_db_and_tables():
    SQLModel.metadata.create_all(pg_engine)


def get_pgpool_session():
    with Session(pg_engine) as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


PgpoolSssionDep = Annotated[Session, Depends(get_pgpool_session)]
