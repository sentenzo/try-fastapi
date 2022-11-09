from functools import cache

from pydantic import BaseSettings, Field, PostgresDsn


class JwtSettings(BaseSettings):
    key: str = Field(env="JWT_KEY")
    algorithm: str = Field(env="JWT_ALGORITHM")
    token_lifespan_minutes: int = Field(
        default=60 * 24 * 365, env="JWT_TOKEN_LIFESPAN_MINUTES"
    )

    class Config:
        env_file = ".env"


class Config(BaseSettings):
    database_url: PostgresDsn
    jwt_settings: JwtSettings = JwtSettings()

    class Config:
        env_file = ".env"


@cache
def get_config():
    return Config()
