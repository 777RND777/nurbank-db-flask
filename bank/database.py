from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///bank/db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    import bank.models
    Base.metadata.create_all(bind=engine)
