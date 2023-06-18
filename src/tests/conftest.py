import uuid

import pytest

from src.domain.entities import User, Transaction
from src.domain.repository import UserRepository, UserUnitOfWork
from src.pkg import security


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = []
        self.transactions = []

    async def create(self, user: User) -> None:
        self.users.append(user)

    async def get_by_id(self, uid: uuid.UUID, for_update: bool = False) -> User | None:
        user_list = [u for u in self.users if u.id == uid]
        if not user_list:
            return None
        return user_list[0]

    async def get_by_username(self, username: str, for_update: bool = False) -> User | None:
        user_list = [u for u in self.users if u.username == username]
        if not user_list:
            return None
        return user_list[0]

    async def create_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    async def update_user(self, user: User) -> None:
        for idx in range(len(self.users)):
            if self.users[idx] == user.id:
                self.users[idx] = user
                break


class InMemoryUserUnitOfWork(UserUnitOfWork):
    def __init__(self):
        self.user_repository: InMemoryUserRepository = InMemoryUserRepository()

    async def __aenter__(self):
        return self

    async def commit(self):
        pass

    async def rollback(self):
        pass


def build_user(username: str = "test", password: str = "test") -> User:
    return User(
        id=uuid.uuid4(),
        username=username,
        password=security.hash_password(password),
        coins=100,
    )


@pytest.fixture(scope="function")
def memory_user_uow() -> InMemoryUserUnitOfWork:
    return InMemoryUserUnitOfWork()
