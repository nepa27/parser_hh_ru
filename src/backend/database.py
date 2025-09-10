import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://alex:alex@localhost/parser_db'

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

async_session = sessionmaker(
    bind=engine,
    class_= AsyncEngine,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
