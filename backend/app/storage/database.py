import logging
from typing import Optional, Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker, Session as SASession, Session

from backend.app.core.settings import db_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self._settings = db_settings
        self._engine: Optional[Engine] = None
        self._SessionLocal: Optional[sessionmaker[SASession]] = None
        self.Base = declarative_base()

    @property
    def engine(self) -> Engine:
        if self._engine is not None:
            self._engine.dispose()
        self._engine = create_engine(self._settings.DATABASE_URL, **self._settings.ENGINE_OPTIONS)
        return self._engine

    @property
    def SessionLocal(self) -> sessionmaker[SASession]:
        if self._SessionLocal is None:
            self._SessionLocal = sessionmaker(bind=self.engine, **self._settings.SESSION_OPTIONS)
        return self._SessionLocal

    def get_db(self) -> Generator[Session, None, None]:
        session = self.get_session()
        try:
            yield session
        finally:
            session.close()

    def get_session(self) -> SASession:
        return self.SessionLocal()

    def check_connection(self) -> None:
        logger.info("Starting up, checking the DB connection")
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except OperationalError as exc:
            logger.error("Failed to connect to the DB (OperationalError): %s", exc)
            raise
        except SQLAlchemyError as exc:
            logger.error("SQLAlchemy error occurred while checking the DB: %s", exc)
            raise
        logger.info("DB connection is OK, proceeding.")



db = Database()
