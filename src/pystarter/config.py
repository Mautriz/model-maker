from functools import cache

from pydantic import BaseSettings


class Config(BaseSettings):
    database_url: str
    debug: bool = False

    class Config:
        env_file_encoding = "utf-8"


@cache
def get_config(env_file: str = ".env") -> Config:
    return Config(_env_file=env_file)  # type: ignore
