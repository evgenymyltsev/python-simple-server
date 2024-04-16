"""Cache is a simple wrapper around Redis to provide string and JSON caching.

This class provides methods to set and get string and JSON values in Redis.

Attributes:
    _redis_client (Redis | None): The Redis client.

    Note:
        The Redis client is lazily initialized.

"""

from typing import Type

from redis import Redis
from redis.commands.json.path import Path

from settings import settings


class Cache:
    """
    Cache is a simple wrapper around Redis to provide string and JSON caching.

    This class provides methods to set and get string and JSON values in Redis.

    Attributes:
        _redis_client (Redis | None): The Redis client.

    Note:
        The Redis client is lazily initialized.

    """

    _redis_client = None

    @classmethod
    def set(cls: Type["Cache"], key: str, value: str | int | float) -> None:
        """Set a string value in Redis.

        Args:
            cls (Type["Cache"]): The class object.
            key (str): The key of the value.
            value (str | int | float): The value to be stored.
        """
        cls._redis_client.set(key, value)

    @classmethod
    def json_set(cls: Type["Cache"], key: str, value: dict) -> None:
        """Set a JSON value in Redis.

        Args:
            cls (Type["Cache"]): The class object.
            key (str): The key of the JSON value.
            value (dict): The JSON value.

        Returns:
            None: This function does not return anything.
        """
        cls._redis_client.json().set(key, Path.root_path(), value)

    @classmethod
    def json_get(cls: Type["Cache"], key: str) -> dict | None:
        """
        Get the value of a Redis JSON key.

        Args:
            cls (Type["Cache"]): The class object.
            key (str): The key to lookup.

        Returns:
            dict or None: The value of the JSON key, or None if the key does not exist.
        """
        return cls._redis_client.json().get(key)

    @classmethod
    def get(cls: Type["Cache"], key: str) -> str | int | float:
        """Get the value of a Redis key.

        Args:
            cls (Type["Cache"]): The class object.
            key (str): The key to lookup.

        Returns:
            str | int | float: The value of the key, or None if the key does not exist.
        """
        return cls._redis_client.get(key)

    @classmethod
    def delete(cls: Type["Cache"], key: str) -> None:
        """Delete the key-value pair from Redis.

        Args:
            cls (Type["Cache"]): The class object.
            key (str): The key of the value to be deleted.

        Returns:
            None: This function does not return anything.
        """
        cls._redis_client.delete(key)

    @classmethod
    def get_all(
        cls: Type["Cache"],
    ) -> dict:
        """Get all key-value pairs from the Redis hash.

        Returns:
            dict: A dictionary containing all the key-value pairs.
        """
        return cls._redis_client.hgetall()

    @classmethod
    def get_redis_client(
        cls: Type["Cache"],
    ) -> Redis:
        """Get a Redis client.

        If the Redis client is not already created, it will be initialized
        using the Redis URL specified in the settings. The Redis client
        is decoded as a string.

        Returns:
            Redis: A Redis client.
        """
        if cls._redis_client is None:
            cls._redis_client = Redis.from_url(settings.redis.redis_dsn, decode_responses=True)
        return cls._redis_client

    @classmethod
    def close_redis_client(
        cls: Type["Cache"],
    ) -> None:
        """Close the Redis client if it is open.

        This method is used to close the Redis client when it is no longer needed.
        It is a good practice to call this method after you have finished using the Redis client.

        Parameters:
            cls (Type["Cache"]): The class object.

        Returns:
            None: This function does not return anything.
        """
        if cls._redis_client:
            cls._redis_client.close()
            cls._redis_client = None
