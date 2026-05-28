from arq import create_pool
from arq.connections import RedisSettings
from app.core.logging import logger
from app.core.settings import settings


class Connection:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Connection, cls).__new__(cls)
            cls._instance.settings = RedisSettings(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                conn_timeout=settings.REDIS_CONNECTION_TIMEOUT,
                retry_on_timeout=True,
            )
        return cls._instance

    async def get_client(self):
        if self._pool is None:
            logger.info("Connecting to ARQ Redis...")
            self._pool = await create_pool(self.settings)
            logger.info("ARQ Redis connected.")
        return self._pool

    async def close(self):
        if self._pool:
            await self._pool.close()
            self._pool = None


connection = Connection()
