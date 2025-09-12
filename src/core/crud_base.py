from typing import Type, Sequence

import asyncio
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.sql import text

from src.core.database import async_engine, async_session, get_db
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

    async def get_all(
            self,
            db: AsyncSession
    ) -> Sequence[Base]:
        """Получает данные из БД."""
        query = await db.execute(select(self.model))
        result = query.scalars().all()
        return result

    async def get_or_404(
            self,
            obj_id: int,
            db: AsyncSession
    ) -> Base:
        """Получает объект из БД по id или выбрасывает 404-ошибку."""
        query = await db.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        result = query.scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Объект {obj_id} в {self.model.__tablename__} не найден')
        return result


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
    # await create_tables(async_engine)

    # await create_data(
    #     User,
    #     {
    #         'first_name': 'name2',
    #         'second_name': 'name2',
    #         'password': 'password',
    #         'email': 'email2',
    #         'is_active': True
    #     }
    # )
    async for session in get_db():
        test_ex = CRUDBase(User)
        await test_ex.get_all(session)
        await test_ex.get_or_404(1, session)


asyncio.run(main())
