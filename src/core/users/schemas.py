from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    first_name: str
    second_name: str
    password: str
    email: str

    class Config:
        orm_mode = True


class UserGetSchema(UserCreateSchema):
    id: int
    is_active: bool
