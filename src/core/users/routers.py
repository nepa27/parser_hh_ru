from fastapi import APIRouter

from src.core.users.schemas import UserCreateSchema, UserGetSchema
from src.core.users.services import UserService
from src.core.users.models import User

router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)


@router.get('')
async def get_users() -> list[UserGetSchema]:
    """Возвращает список пользователей."""
    return await UserService(User).get_all()


@router.get('/{user_id}')
async def get_one_user(user_id: int) -> UserGetSchema:
    """Возвращает одного пользователя."""
    return await UserService(User).get_one_or_none(user_id)


@router.post('/create')
async def create_users(user_data: UserCreateSchema):
    """Создает пользователя."""
    return await UserService(User).create(user_data.dict())
