from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from src.core.base.models import Base


class ChatData(Base):
    """Модель чата."""

    __tablename__ = 'chat_data'

    id = Column(Integer, primary_key=True, index=True)
    chat_vacancy = Column(String, nullable=False)
    chat_company = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('submits.id'))

    users = relationship('User', back_populates='chat_data')
    submits = relationship('Submit', back_populates='chat_data')
    user_chats = relationship('UserChat', back_populates='chat_data')


class UserChat(Base):
    """Модель сообщения из чатов."""

    __tablename__ = 'user_chats'

    id = Column(Integer, primary_key=True, index=True)
    name_company = Column(String, nullable=False)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    time = Column(Time, nullable=False)
    date = Column(String, nullable=False)
    type = Column(String, nullable=False)

    chat_id = Column(Integer, ForeignKey('chat_data.id'))

    chat_data = relationship('ChatData', back_populates='user_chats')
