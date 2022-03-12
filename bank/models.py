from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base, session


class User(Base):
    __tablename__ = "users"

    pk = Column(Integer, primary_key=True)
    id = Column(Integer, unique=True, nullable=False)
    password_hash = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    nickname = Column(String(250), nullable=False)
    debt = Column(Integer, nullable=False, default=0)

    applications = relationship("Application", back_populates="user", lazy=True)

    @classmethod
    def get_list(cls):
        users = cls.query.all()
        session.commit()
        return users

    @classmethod
    def get(cls, user_id: int):
        user = cls.query.filter(cls.id == user_id).first()
        session.commit()
        return user

    def save(self):
        session.add(self)
        session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class Application(Base):
    __tablename__ = "applications"

    pk = Column(Integer, primary_key=True)
    id = Column(Integer, unique=True, nullable=False)
    value = Column(Integer, nullable=False)
    request_date = Column(String(50), nullable=False)
    answer_date = Column(String(50), nullable=False, default='')
    approved = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="applications", lazy=True)

    @classmethod
    def get_user_list(cls, user_id: int):
        applications = cls.query.filter(cls.user_id == user_id).all()
        session.commit()
        return applications

    @classmethod
    def get(cls, application_id: int):
        application = cls.query.filter(cls.id == application_id).first()
        session.commit()
        return application

    def save(self):
        session.add(self)
        session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()
