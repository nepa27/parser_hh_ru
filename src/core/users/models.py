from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.core.base.models import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, unique=True)
    second_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)

    chat_data = relationship('ChatData', back_populates='users')
    submits = relationship('Submit', back_populates='users')


from src.core.chats.models import ChatData
from src.core.submits.models import Submit
