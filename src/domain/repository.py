from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import User, Transaction


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str, for_update: bool = False) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, uid: UUID, for_update: bool = False) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_transaction(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError


class UserUnitOfWork(ABC):
    user_repository: UserRepository

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
