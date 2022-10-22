from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from ..utils.db_url_builder import DbUrlEnvBuilder, DbUrlParams

ENV_MAPPING = {
    DbUrlParams.PROTOCOL: "DB_PROTOCOL",
    DbUrlParams.DRIVER: "DB_DRIVER",
    DbUrlParams.USER: "DB_USER",
    DbUrlParams.PASSWPRD: "DB_PASSWORD",
    DbUrlParams.HOST: "DB_HOST",
    DbUrlParams.PORT: "DB_PORT",
    DbUrlParams.DBNAME: "DB_DBNAME",
}

DbUriBuilderLocal = DbUrlEnvBuilder.get_local_type(ENV_MAPPING)


class SessionManager:
    def __init__(self) -> None:
        self.engine: Engine = None
        self.refresh()

    def __new__(cls: type[SessionManager]) -> SessionManager:
        # sort-of singleton
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    def refresh(self):
        sql_db_url = DbUriBuilderLocal().from_env().to_str()
        self.engine = create_async_engine(sql_db_url)

    @property
    def SessionLocal(self):
        return sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )


async def get_session_dependency() -> AsyncSession:
    SessionLocal = SessionManager().SessionLocal
    async with SessionLocal() as session:
        yield session


__all__ = [DbUriBuilderLocal, get_session_dependency]
