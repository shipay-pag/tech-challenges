from sqlalchemy import select, update

from infrastructure.database.sql import Base
from infrastructure.repositories.irepository import IRepository


class SqlRepository(IRepository):
    model = Base

    async def get_all(self):
        async with self.session_factory() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def filter_by(self, params):
        async with self.session_factory() as session:
            result = await session.execute(select(self.model).filter_by(**params))
            return result.scalars().first()

    async def filter_all_by(self, params):
        async with self.session_factory() as session:
            result = await session.execute(select(self.model).filter_by(**params))
            return result.scalars()

    async def create(self, values):
        async with self.session_factory() as session:
            _model = self.model(**values)
            session.add(_model)
            await session.commit()
            return _model

    async def update(self, pk, values):
        async with self.session_factory() as session:
            await session.execute(update(self.model).where(self.model.id == pk).values(**values))
            await session.commit()

    async def delete(self, _model: Base):
        async with self.session_factory() as session:
            await session.delete(_model)
            await session.commit()

    async def commit(self):
        async with self.session_factory() as session:
            await session.commit()

    async def rollback(self):
        async with self.session_factory() as session:
            await session.rollback()
