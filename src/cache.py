from typing import Union

from redis import Redis
from redis.commands.json.path import Path

from config import REDIS_URL


class Cache:
    _redis_client = None

    @classmethod
    def set(cls, key: str, value: Union[str, int, float]) -> None:
        cls._redis_client.set(key, value)

    @classmethod
    def json_set(cls, key: str, value: dict) -> None:
        cls._redis_client.json().set(key, Path.root_path(), value)

    @classmethod
    def json_get(cls, key: str) -> dict:
        return cls._redis_client.json().get(key)

    @classmethod
    def get(cls, key: str) -> Union[str, int, float]:
        return cls._redis_client.get(key)

    @classmethod
    def delete(cls, key: str) -> None:
        cls._redis_client.delete(key)

    @classmethod
    def get_all(cls) -> dict:
        return cls._redis_client.hgetall()

    @classmethod
    def get_redis_client(cls) -> Redis:
        if cls._redis_client is None:
            cls._redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
        return cls._redis_client

    @classmethod
    def close_redis_client(cls) -> None:
        if cls._redis_client:
            cls._redis_client.close()
            cls._redis_client = None
