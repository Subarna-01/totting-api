import redis.asyncio as redis
from app.core.logging import logger
from app.core.settings import settings


class Connection:
    _instance = None
    _client: redis.Redis | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance

    async def connect(self):
        if self._client is None:
            logger.info("Connecting to Redis...")

            self._client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=getattr(settings, "REDIS_PASSWORD", None),
                decode_responses=True,
                socket_connect_timeout=settings.REDIS_CONNECTION_TIMEOUT,
                retry_on_timeout=True,
            )

            try:
                await self._client.ping()
                logger.info("Redis connected successfully.")
            except Exception as e:
                logger.error(f"Redis connection failed: {str(e)}")
                raise

        return self._client

    async def get_client(self):
        if self._client is None:
            return await self.connect()
        return self._client

    async def close(self):
        if self._client:
            logger.info("Closing Redis connection...")
            await self._client.close()
            self._client = None
            logger.info("Redis connection closed.")


connection = Connection()
