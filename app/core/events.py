import time
from app.core.arq.connection import connection as arq_conn
from app.core.database.base import USERS_DB_BASE, GAMES_DB_BASE
from app.core.database.connection import connection as db_conn
from app.core.redis.connection import connection as redis_conn
from app.core.logging import logger
from app.core.settings import settings

DB_NAMES = [settings.USERS_DB, settings.GAMES_DB]
DB_BASES = [USERS_DB_BASE, GAMES_DB_BASE]


async def startup():
    s = time.time()
    logger.info("Preparing resources...")

    db_conn.init_engines(DB_NAMES)

    for db_name, Base in zip(DB_NAMES, DB_BASES):
        engine = db_conn.get_engine(db_name)
        Base.metadata.create_all(bind=engine)

    # await redis_conn.connect()
    # await arq_conn.get_client()

    e = time.time()
    logger.info(f"Resources preparation complete in {e - s:.2f}s.")


async def shutdown():
    s = time.time()
    logger.info("Cleaning up resources...")

    await db_conn.close()
    # await redis_conn.close()
    # await arq_conn.close()

    e = time.time()
    logger.info(f"Resources cleanup complete in {e - s:.2f}s.")
