from asyncio import current_task
from contextlib import asynccontextmanager
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from config import Config
from infrastructure.database.idatabase import IDatabase

Base = declarative_base()

class PostgresDatabase(IDatabase):

    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=False, pool_size=int(Config.SQL_POOL_SIZE),
                                           max_overflow=int(Config.SQL_MAX_OVERFLOW))
        self._session_factory = async_scoped_session(
            orm.sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession), scopefunc=current_task)

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @asynccontextmanager
    async def session(self):
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
