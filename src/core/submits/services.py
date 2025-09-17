from sqlalchemy import func, select

from src.core.base.crud_base import CRUDBase
from src.core.db.database import async_session
from src.core.submits.models import SubmitType
from src.core.submits.schemas import SubmitAggregateSchema


class SubmitService(CRUDBase):
    """Реализует методы CRUD с откликами."""

    async def get_all(self) -> SubmitAggregateSchema:
        """Получает данные из БД."""
        async with async_session() as session:
            total_submits_query = select(
                func.count(self.model.id)).select_from(self.model
                                                       )

            refusal_count_query = select(
                func.count()
            ).where(self.model.type_submit == SubmitType.REFUSAL).select_from(
                self.model
            )
            invitation_count_query = select(
                func.count()
            ).where(self.model.type_submit == SubmitType.INVITATION).select_from(
                self.model
            )
            viewed_count_query = select(
                func.count()
            ).where(self.model.type_submit == SubmitType.VIEWED).select_from(
                self.model
            )

            results = await session.execute(
                select(
                    total_submits_query.label('total_submits'),
                    refusal_count_query.label('refusal_count'),
                    invitation_count_query.label('invitation_count'),
                    viewed_count_query.label('viewed_count')
                )
            )

            row = results.fetchone()
        return SubmitAggregateSchema(
            total_submits=row.total_submits,
            refusal_count=row.refusal_count,
            invitation_count=row.invitation_count,
            viewed_count=row.viewed_count
        )
