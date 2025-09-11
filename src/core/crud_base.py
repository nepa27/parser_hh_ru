from typing import Type

import asyncio
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text

from src.core.database import async_engine, async_session
from src.core.models import Base, User


class CRUDBase:
    """Универсальный базовый класс для CRUD операций."""

    def __init__(self, model: Type[Base]):
        """
        Инициализирует CRUD-класс с указанной моделью.

        Параметры:
            model: SQLAlchemy-модель (класс), связанный с таблицей в БД.
        """
        self.model = model

    async def get_all(self) -> list[tuple]:
        """Функция получения всех данных."""
        async with async_engine.connect() as conn:
            query = select(self.model)
            result = await conn.execute(query)
            data = result.all()
            print(data)
            return data


async def check_db_connection(engine: AsyncEngine) -> None:
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text('SELECT version();'))
            db_version = result.scalar_one()
            print(f'База данных подключена. Версия: {db_version}')
    except Exception as e:
        print(f'Ошибка при подключении к БД: {e}')


async def create_tables(engine: AsyncEngine) -> None:
    """Функция создания таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables(engine: AsyncEngine) -> None:
    """Функция удаления таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_data(model: Type[Base], data: dict) -> None:
    """Функция добавления данных в таблицу."""
    async with async_session() as session:
        try:
            session.add(model(**data))
            await session.commit()
        except IntegrityError as e:
            detail = (e.args[-1]).split('DETAIL:')[-1].strip()
            print(f'Ошибка при добавлении данных. {detail}\n')
            await session.rollback()


async def main() -> None:
    await check_db_connection(async_engine)

    # await delete_tables(async_engine)
    await create_tables(async_engine)

    await create_data(
        User,
        {
            'first_name': 'name2',
            'second_name': 'name2',
            'password': 'password',
            'email': 'email2',
            'is_active': True
        }
    )
    test_ex = CRUDBase(User)
    await test_ex.get_all()


asyncio.run(main())
