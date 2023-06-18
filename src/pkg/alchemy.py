from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

from src import conf

Base = declarative_base()
engine = create_async_engine(conf.DATABASE_URL)

session_factory = async_sessionmaker(engine)
