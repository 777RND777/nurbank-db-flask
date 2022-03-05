from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base, session


class User(Base):
    __tablename__ = "users"

    pk = Column(Integer, primary_key=True)
    id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    username = Column(String(250))
    nickname = Column(String(250))
    debt = Column(Integer, default=0)

    applications = relationship("Application", back_populates="user", lazy=True)

    @classmethod
    def get_list(cls):
        try:
            users = cls.query.all()
            session.commit()
            return users
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get(cls, user_id: int):
        try:
            user = cls.query.filter(cls.id == user_id).first()
            session.commit()
            return user
        except Exception:
            session.rollback()
            raise

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


class Application(Base):
    __tablename__ = "applications"

    pk = Column(Integer, primary_key=True)
    id = Column(Integer, unique=True, nullable=False)
    value = Column(Integer, nullable=False)
    request_date = Column(String(50), nullable=False)
    answer_date = Column(String(50))
    approved = Column(Boolean, default=False)
    is_admin = Column(Boolean)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="applications", lazy=True)

    @classmethod
    def get_list(cls):
        try:
            applications = cls.query.all()
            session.commit()
            return applications
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get_user_list(cls, user_id: int):
        try:
            applications = cls.query.filter(cls.user_id == user_id).all()
            session.commit()
            return applications
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get(cls, application_id: int):
        try:
            user = cls.query.filter(cls.id == application_id).first()
            session.commit()
            return user
        except Exception:
            session.rollback()
            raise

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
