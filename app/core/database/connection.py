from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Dict
from app.core.logging import logger
from app.core.settings import settings


class Connection:
    _instance = None
    _engines: Dict[str, any] = {}
    _sessions: Dict[str, any] = {}
    DATABASE_URL: str = (
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASS}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}"
    )

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_engines(self, db_names):
        logger.info("Initializing databases...")
        for db_name in db_names:
            engine = create_engine(
                f"{self.DATABASE_URL}/{db_name}",
                echo=False,
                future=True,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                isolation_level="READ COMMITTED",
                connect_args={
                    "connect_timeout": settings.DB_CONNECTION_TIMEOUT,
                },
            )

            try:
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                logger.info(f"Database: {db_name} connected successfully.")
            except Exception as e:
                logger.error(f"Database: {db_name} connection failed: {str(e)}")
                raise

            SessionLocal = sessionmaker(bind=engine)
            self._engines[db_name] = engine
            self._sessions[db_name] = SessionLocal

        logger.info("Database initialization complete.")

    def get_engine(self, db_name):
        return self._engines.get(db_name)

    def get_session(self, db_name):
        return self._sessions.get(db_name)

    async def close(self):
        logger.info("Closing databases...")
        for engine in self._engines.values():
            await engine.dispose()
        logger.info("Databases closed successfully.")


connection = Connection()
