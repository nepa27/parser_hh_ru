from fastapi import APIRouter

from src.core.submits.models import Submit
from src.core.submits.schemas import SubmitGetSchema, SubmitCreateSchema, SubmitAggregateSchema
from src.core.submits.services import SubmitService

router = APIRouter(
    prefix='/submits',
    tags=['Отклики']
)


@router.get('')
async def get_number_of_submits() -> SubmitAggregateSchema:
    """Возвращает количество откликов."""
    return await SubmitService(Submit).get_all()


@router.get('/{submit_id}')
async def get_one_submit(submit_id: int) -> SubmitGetSchema | None:
    """Возвращает один отклик."""
    data = await SubmitService(Submit).get_one_or_none(submit_id)
    return data


@router.post('/add')
async def add_submit(user_data: SubmitCreateSchema):
    """Добавляет отклик."""
    return await SubmitService(Submit).create(user_data.dict())
