from dependency_injector import containers, providers
from config import Config
from endpoints.health.repository import HealthSqlRepository
from endpoints.health.service import HealthService

from endpoints.registration.repository import RegistrationRepository
from endpoints.registration.service import RegistrationService
from endpoints.registration.manager import Orchestrator

from infrastructure.database.sql import PostgresDatabase
from infrastructure.repositories.sql_repository import SqlRepository



class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres_database = providers.Singleton(PostgresDatabase, db_url=Config.POSTGRES_DATABASE_URL)

    health_sql_repository = providers.Factory(HealthSqlRepository, session_factory=postgres_database.provided.session)
    health_service = providers.Factory(HealthService, sql_repository=health_sql_repository)

    registration_repository = providers.Factory(RegistrationRepository, session_factory=postgres_database.provided.session)
    registration_service = providers.Factory(RegistrationService, sql_repository=registration_repository)
    registration_orchestrator = providers.Factory(Orchestrator, sql_repository=registration_repository, service=registration_service)
