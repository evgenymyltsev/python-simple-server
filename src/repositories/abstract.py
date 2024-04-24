"""This module defines an abstract base class for Repository implementations."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import insert, select, update

from src.database import async_session


class AbstractRepository(ABC):
    """Abstract class for Repository implementations.

    This class serves as the base for all repository implementations. It defines
    abstract methods that must be implemented by any class inheriting from it.

    Attributes:
        model (DeclarativeBase): The SQLAlchemy declarative base class representing
            the database model.

    Methods:
        add_one(): Add a new instance of the model to the database.
        find_one(filter_by): Retrieve a single instance of the model from the database,
            filtered by the given attributes.
        find_all(): Retrieve all instances of the model from the database.
        update_one(): Update a single instance of the model in the database.
        delete_one(): Delete a single instance of the model from the database.
    """

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


T = TypeVar("T")


class SQLAlchemyRepository(AbstractRepository, Generic[T]):
    """SQLAlchemyRepository is a concrete implementation of AbstractRepository for SQLAlchemy ORM.

    Attributes:
        model: A SQLAlchemy ORM model that this repository handles.
    """

    model: T | None = None

    async def add_one(self: "SQLAlchemyRepository", data: dict) -> T:
        """
        Add a new instance of the model to the database.

        Args:
            data (dict): A dictionary containing the data to be inserted into the database.

        Returns:
            T: The newly created instance of the model.
        """
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            model = res.scalar_one()
            return model

    async def find_one(self: "SQLAlchemyRepository", filter_by: dict) -> T | None:
        """
        Retrieve a single instance of the model from the database, filtered by the given attributes.

        Args:
            filter_by (dict): A dictionary of attribute names and values to filter by.

        Returns:
            T: The instance of the model that matches the given filter, or None if no match is found.
        """
        async with async_session() as session:
            query = select(self.model).filter_by(**filter_by)
            res = await session.execute(query)
            model = res.scalar_one()
            return model

    async def find_all(self: "SQLAlchemyRepository") -> list[T] | None:
        """
        Retrieve all instances of the model from the database.

        Returns:
            list[T] | None: A list of all instances of the model, or None if no instances are found.
        """
        async with async_session() as session:
            query = select(self.model)
            res = await session.execute(query)
            models = res.scalars().all()
            return models

    async def update_one(self: "SQLAlchemyRepository", filter_by: dict, data: dict) -> T | None:
        """
        Update a single instance of the model in the database, filtered by the given attributes.

        Args:
            filter_by (dict): A dictionary of attribute names and values to filter by.
            data (dict): A dictionary containing the data to be updated.

        Returns:
            T | None: The instance of the model that was updated, or None if no match is found.
        """
        async with async_session() as session:
            stmt = update(self.model).filter_by(**filter_by).values(**data).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()
            model = result.scalar()
            return model

    async def delete_one(self: "SQLAlchemyRepository", filter_by: dict) -> T | None:
        """
        Delete a single instance of the model from the database, filtered by the given attributes.

        Args:
            filter_by (dict): A dictionary of attribute names and values to filter by.

        Returns:
            T | None: The instance of the model that was deleted, or None if no match is found.
        """
        async with async_session() as session:
            query = select(self.model).filter_by(**filter_by)
            res = await session.execute(query)
            model = res.scalar_one()
            await session.delete(model)
            await session.commit()
            return model
