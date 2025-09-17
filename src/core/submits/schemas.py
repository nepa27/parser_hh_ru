from pydantic import BaseModel

from src.core.submits.models import SubmitType


class SubmitCreateSchema(BaseModel):
    type_submit: SubmitType

    class Config:
        from_attributes = True


class SubmitGetSchema(SubmitCreateSchema):
    id: int


class SubmitAggregateSchema(BaseModel):
    total_submits: int
    refusal_count: int
    invitation_count: int
    viewed_count: int
