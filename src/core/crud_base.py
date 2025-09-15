from typing import Type, Sequence

import asyncio
from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.sql import text

from src.core.config.logging import logger
from src.core.database import async_engine, get_db
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
            session: AsyncSession
    ) -> Sequence[Base]:
        """Получает данные из БД."""
        query = await session.execute(select(self.model))
        result = query.scalars().all()
        # TODO: Удалить позже
        for res in result:
            print((res.id, res.second_name))
        return result

    async def get_or_404(
            self,
            session: AsyncSession,
            obj_id: int
    ) -> Base:
        """Получает объект из БД по id или выбрасывает 404-ошибку."""
        query = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        result = query.scalars().first()
        if not result:
            message = f'Объект {obj_id} в {self.model.__tablename__} не найден'
            logger.error(message)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message)
        return result

    async def create(
            self,
            session: AsyncSession,
            data: dict
    ) -> Base:
        """Добавляет данные в БД."""
        db_obj = self.model(**data)
        try:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj
        except Exception as e:
            logger.error(f'Ошибка при добавлении данных в БД: {e}')
            await session.rollback()

    async def update(
            self,
            session: AsyncSession,
            data: dict,
            obj_id: int
    ) -> None:
        """Обновляет данные в БД."""
        try:
            query = (
                update(self.model)
                .values(**data)
                .filter_by(id=obj_id)
            )
            await session.execute(query)
            await session.commit()
        except Exception as e:
            logger.error(f'Ошибка при обновлении данных в БД: {e}')
            await session.rollback()

    async def delete(
            self,
            session: AsyncSession,
            db_object: Base
    ) -> None:
        """Удаляет данные из БД."""
        try:
            await session.delete(db_object)
            await session.commit()
        except Exception as e:
            logger.error(f'Ошибка при удалении данных в БД: {e}')
            await session.rollback()

    @staticmethod
    async def check_db_connection(engine: AsyncEngine) -> None:
        try:
            async with engine.connect() as connection:
                result = await connection.execute(text('SELECT version();'))
                db_version = result.scalar_one()
                logger.info(f'База данных подключена. Версия: {db_version}')
        except Exception as e:
            logger.info(f'Ошибка при подключении к БД: {e}')

    @staticmethod
    async def create_tables(engine: AsyncEngine) -> None:
        """Функция создания таблиц."""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def delete_tables(engine: AsyncEngine) -> None:
        """Функция удаления таблиц."""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


async def main() -> None:
    # await delete_tables(async_engine)
    # await create_tables(async_engine)

    # await create_data(
    #     User,
    data = {
        'first_name': 'name3',
        'second_name': 'name3',
        'password': 'password',
        'email': 'email3',
        'is_active': True
    }
    new_data = {
        'second_name': 'name56',
    }

    # )
    async for session in get_db():
        test_ex = CRUDBase(User)
        await test_ex.check_db_connection(async_engine)
        await test_ex.get_all(session)


asyncio.run(main())
