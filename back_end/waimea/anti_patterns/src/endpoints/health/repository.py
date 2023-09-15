from infrastructure.repositories.sql_repository import SqlRepository


class HealthSqlRepository(SqlRepository):
    async def get_health(self) -> bool:
        async with self.session_factory() as session:
            await session.execute('SELECT NOW()')
            return True

