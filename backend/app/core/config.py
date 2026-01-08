from pydantic_settings import BaseSettings

class BaseAppSettings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    ENVIRONMENT: str

    class Config:
        env_file = "dev.env"
        env_file_encoding = "utf-8"
        extra = "ignore"

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
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def ENGINE_OPTIONS(self) -> dict:
        return {
            "echo": self.SQLALCHEMY_ECHO,
            "pool_size": self.SQLALCHEMY_POOL_SIZE,
            "max_overflow": self.SQLALCHEMY_MAX_OVERFLOW,
            "pool_recycle": self.SQLALCHEMY_POOL_RECYCLE,
        }

    @property
    def SESSION_OPTIONS(self) -> dict:
        return {
            "autocommit": self.SQLALCHEMY_AUTOCOMMIT,
            "autoflush": self.SQLALCHEMY_AUTOFLUSH,
        }

class FastAPISettings(BaseAppSettings):
    HOST: str
    PORT: int
    RELOAD: bool
