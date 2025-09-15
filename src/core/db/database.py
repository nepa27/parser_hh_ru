from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')
DB_NAME = getenv('DB_NAME')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)
