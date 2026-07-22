from config import settings
from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends
database_url = ("postgresql+psycopg://"
f"{settings.database_user}:"
f"{settings.database_password}@"
f"{settings.database_host}/"
f"{settings.database_db}")
engine=create_engine(database_url,echo=True)
def create_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session,Depends(create_session)]