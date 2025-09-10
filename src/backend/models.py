from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, unique=True)
    second_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)

    chat_data = relationship('ChatData', back_populates='users')
    submits = relationship('Submit', back_populates='users')


class ChatData(Base):
    __tablename__ = 'chat_data'

    id = Column(Integer, primary_key=True, index=True)
    chat_vacancy = Column(String, nullable=False)
    chat_company = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('submits.id'))

    users = relationship('User', back_populates='chat_data')
    submits = relationship('Submit', back_populates='chat_data')
    user_chats = relationship('UserChat', back_populates='chat_data')


class Submit(Base):
    __tablename__ = 'submits'

    id = Column(Integer, primary_key=True, index=True)
    number_of_submits = Column(Integer, nullable=False)
    refusal = Column(Integer, nullable=False)
    invitation = Column(Integer, nullable=False)
    viewed = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))

    users = relationship('User', back_populates='submits')
    chat_data = relationship('ChatData', back_populates='submits')


class UserChat(Base):
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
