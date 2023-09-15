from endpoints.health.repository import HealthSqlRepository


class HealthService:
    def __init__(self, sql_repository: HealthSqlRepository) -> None:
        self._sql_repository = sql_repository

    async def get_health_status(self) -> dict:
        healthcheck = dict()
        healthcheck['postgres'] = await self.__ping_postgres_db()
        return healthcheck

    async def __ping_postgres_db(self):
        try:
            await self._sql_repository.get_health()
            return True
        except Exception as e:
            return False
