from os import getenv


class Config:
    APP_ENV = getenv('APP_ENV', 'local')

    REQUEST_TIMEOUT = int(getenv('REQUEST_TIMEOUT', 10))

    POSTGRES_DATABASE_URL = getenv(
        'ASYNC_POSTGRES_DATABASE_URL', 'postgresql+asyncpg://sem:senha@localhost:5432/monte_de_dados')

    MAX_ITEMS_PER_PAGE = int(getenv('MAX_ITEMS_PER_PAGE', 1000))
    DEFAULT_ITEMS_PER_PAGE = int(getenv('DEFAULT_ITEMS_PER_PAGE', 500))

    SQL_POOL_SIZE = getenv('SQL_POOL_SIZE', 5)
    SQL_MAX_OVERFLOW = getenv('SQL_MAX_OVERFLOW', 10)

