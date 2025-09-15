from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.core.base.models import Base


class Submit(Base):
    """Модель откликов."""

    __tablename__ = 'submits'

    id = Column(Integer, primary_key=True, index=True)
    number_of_submits = Column(Integer, nullable=False)
    refusal = Column(Integer, nullable=False)
    invitation = Column(Integer, nullable=False)
    viewed = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))

    users = relationship('User', back_populates='submits')
    chat_data = relationship('ChatData', back_populates='submits')
