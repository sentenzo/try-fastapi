"""
A couple of tools for building a database URL (dialect[+driver]://user:password@host:port/dbname).

Examples of such URLs:
    postgresql://scott:tiger@localhost/test
    mysql+pymysql://scott:tiger@localhost/foo
    oracle://scott:tiger@127.0.0.1:1521/sidname

Application examples:
    env_mapping = {
        DbUrlParams.PROTOCOL: "DB_PROTOCOL",
        DbUrlParams.USER: "DB_USER",
        DbUrlParams.PASSWPRD: "DB_PASSWORD",
        DbUrlParams.HOST: "DB_HOST",
        DbUrlParams.PORT: "DB_PORT",
    #    DbUrlParams.DBNAME: "DB_DBNAME",
    }

    DbUriBuilderLocal = DbUrlEnvBuilder.get_local_type(env_mapping)
    ldub: DbUrlEnvBuilder = DbUriBuilderLocal()
    ldub.from_env()
    ldub.host("192.168.0.14").port(6776)
    ldub.dbname("my_db_name")
    SQL_DATABASE_URL = ldub.to_str()
"""

from __future__ import annotations
from enum import Enum
import os
from typing import Any, Callable
import logging

logger = logging.getLogger(__name__)


class DbUrlParams(Enum):
    PROTOCOL = "protocol"
    DRIVER = "driver"
    USER = "user"
    PASSWPRD = "password"
    HOST = "host"
    PORT = "port"
    DBNAME = "dbname"


class DbUrlBuilder:
    def __init__(
        self,
        protocol=None,
        driver=None,
        user=None,
        password=None,
        host=None,
        port=None,
        dbname=None,
    ):
        self._protocol = protocol
        self._driver = driver
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._dbname = dbname

    def protocol(self, protocol):
        self._protocol = protocol
        return self

    def driver(self, driver):
        self._driver = driver
        return self

    def user(self, user):
        self._user = user
        return self

    def password(self, password):
        self._password = password
        return self

    def host(self, host):
        self._host = host
        return self

    def port(self, port):
        self._port = port
        return self

    def dbname(self, dbname):
        self._dbname = dbname
        return self

    def to_str(self):
        # f"postgresql://{user}:{passwd}@{host}:{dbport}/{dbname}"
        if None in (self._protocol, self._user, self._host):
            raise ValueError()
        db_conn_url = [self._protocol]
        if self._driver:
            db_conn_url.extend(["+", self._driver])
        db_conn_url.extend(["://", self._user])
        if self._password:
            db_conn_url.extend([":", self._password])
        db_conn_url.extend(["@", self._host])
        if self._port:
            db_conn_url.extend([":", self._port])
        if self._dbname:
            db_conn_url.extend(["/", self._dbname])
        return "".join(db_conn_url)

    def __repr__(self) -> str:
        params = None
        msg = ""
        try:
            params = f"    DbUrl:     {self.to_str()}"
        except ValueError:
            params = (
                f"    protocol:  {self._protocol}\n"
                f"    user:      {self._user}\n"
                f"    password:  {None if self._password == None else '******'}\n"
                f"    host:      {self._host}\n"
                f"    port:      {self._port}\n"
                f"    dbname:    {self._dbname}"
            )
            msg = " - not enough parameters to form a DB URL!"
        return f"{self.__class__.__name__}(\n{params}\n){msg}"


class DbUrlEnvBuilder(DbUrlBuilder):
    @staticmethod
    def _default_env_mapping_gen() -> dict[DbUrlParams, str]:
        return {}

    @staticmethod
    def get_local_type(env_mapping: dict[DbUrlParams, str]) -> type[DbUrlEnvBuilder]:
        class DbUrlEnvBuilderLocal(DbUrlEnvBuilder):
            @staticmethod
            def _default_env_mapping_gen() -> dict[DbUrlParams, str]:
                return env_mapping.copy()

        return DbUrlEnvBuilderLocal

    def __init__(
        self,
        protocol=None,
        driver=None,
        user=None,
        password=None,
        host=None,
        port=None,
        dbname=None,
        ###
        env_mapping: dict[DbUrlParams, str] = None,
    ):
        super().__init__(protocol, driver, user, password, host, port, dbname)
        self._env_mapping = env_mapping or self.__class__._default_env_mapping_gen()
        self._env_param_calls: dict[DbUrlParams, Callable] = {
            DbUrlParams.PROTOCOL: self.env_protocol,
            DbUrlParams.DRIVER: self.env_driver,
            DbUrlParams.USER: self.env_user,
            DbUrlParams.PASSWPRD: self.env_password,
            DbUrlParams.HOST: self.env_host,
            DbUrlParams.PORT: self.env_port,
            DbUrlParams.DBNAME: self.env_dbname,
        }

    @staticmethod
    def _env_warpper(method, env_var: str) -> DbUrlEnvBuilder:
        return method(os.environ.get(env_var, None))

    def env_protocol(self, env_var):
        return DbUrlEnvBuilder._env_warpper(super().protocol, env_var)

    def env_driver(self, env_var):
        return DbUrlEnvBuilder._env_warpper(super().driver, env_var)

    def env_user(self, env_var):
        return DbUrlEnvBuilder._env_warpper(super().user, env_var)

    def env_password(self, env_var):
        return DbUrlEnvBuilder._env_warpper(super().password, env_var)

    def env_host(self, env_var):
        return DbUrlEnvBuilder._env_warpper(super().host, env_var)

    def env_port(self, env_var):
        return DbUrlEnvBuilder._env_warpper(super().port, env_var)

    def env_dbname(self, env_var):
        return DbUrlEnvBuilder._env_warpper(super().dbname, env_var)

    def _env_param(self, param: DbUrlParams, env_var):
        return self._env_param_calls[param](env_var)

    def from_env(self, env_mapping: dict[DbUrlParams, str] = None) -> DbUrlEnvBuilder:
        env_mapping = env_mapping or self._env_mapping
        for key, env_val in env_mapping.items():
            try:
                param = key
                if isinstance(key, str):
                    param = DbUrlParams(str(key))  # maybe throws ValueError
                self._env_param(param, env_val)
            except ValueError:
                continue
        return self
