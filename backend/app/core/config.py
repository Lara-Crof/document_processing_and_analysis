from pydantic_settings import BaseSettings

class BaseAppSettings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    ENVIRONMENT: str

    class Config:
        env_file = "dev.env"
        env_file_encoding = "utf-8"


class DatabaseSettings(BaseAppSettings):
    # PostgreSQL
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # SQLAlchemy
    SQLALCHEMY_ECHO: bool
    SQLALCHEMY_POOL_SIZE: int
    SQLALCHEMY_MAX_OVERFLOW: int
    SQLALCHEMY_POOL_RECYCLE: int

    # SQLAlchemy session
    SQLALCHEMY_AUTOCOMMIT: bool
    SQLALCHEMY_AUTOFLUSH: bool

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class FastAPISettings(BaseAppSettings):
    HOST: str
    PORT: int
    RELOAD: bool
