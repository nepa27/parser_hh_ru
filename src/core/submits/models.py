from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.core.base.models import Base


class SubmitType(PyEnum):
    REFUSAL = 'refusal'
    INVITATION = 'invitation'
    VIEWED = 'viewed'


class Submit(Base):
    """Модель откликов."""

    __tablename__ = 'submits'

    id = Column(Integer, primary_key=True, index=True)
    type_submit = Column(Enum(SubmitType))

    user_id = Column(Integer, ForeignKey('users.id'))

    users = relationship('User', back_populates='submits')
    chat_data = relationship('ChatData', back_populates='submits')
