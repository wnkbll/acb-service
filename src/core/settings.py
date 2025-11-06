from functools import lru_cache
from typing import Any
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import ENV_PATH

settings_config_dict = SettingsConfigDict(
    env_file=ENV_PATH,
    env_file_encoding="utf-8",
    validate_default=False,
    extra="ignore",
)


class PostgresSettings(BaseSettings):
    model_config = settings_config_dict

    user: str = Field(validation_alias="DB_USER")
    password: str = Field(validation_alias="DB_PASS")
    host: str = Field(validation_alias="DB_HOST")
    port: str = Field(validation_alias="DB_PORT")
    name: str = Field(validation_alias="DB_NAME")


class FastAPISettings(BaseModel):
    debug: bool = True
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "ACB service"
    version: str = "0.1.0"


class MiddlewareSettings(BaseModel):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class Settings(BaseModel):
    postgres: PostgresSettings = PostgresSettings()  # type: ignore

    fastapi: FastAPISettings = FastAPISettings()
    middleware: MiddlewareSettings = MiddlewareSettings()

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres.user}:{self.postgres.password}@"
            f"{self.postgres.host}:{self.postgres.port}/"
            f"{self.postgres.name}"
        )

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return self.fastapi.model_dump()

    @property
    def middleware_kwargs(self) -> dict[str, Any]:
        return self.middleware.model_dump()


@lru_cache
def get_app_settings() -> Settings:
    return Settings()
