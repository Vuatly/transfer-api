from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import User, Transaction
from src.domain.repository import UserRepository, UserUnitOfWork
from src.infra.models import UserDB, TransactionDB
from src.pkg.alchemy import session_factory


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: User) -> None:
        user_db = UserDB(**asdict(user))
        self._session.add(user_db)

    async def get_by_username(self, username: str, for_update: bool = False) -> User | None:
        stmt = select(UserDB).where(UserDB.username == username)

        if for_update:
            stmt = stmt.with_for_update()

        res = await self._session.execute(stmt)
        user_db = res.scalars().one_or_none()

        if user_db:
            return self._build_user(user_db)

    async def get_by_id(self, uid: UUID, for_update: bool = False) -> User | None:
        user_db = await self._session.get(UserDB, uid, with_for_update=for_update)

        if user_db:
            return self._build_user(user_db)

    async def create_transaction(self, transaction: Transaction) -> None:
        transaction_db = TransactionDB(
            id=transaction.id,
            sender_id=transaction.sender.id,
            recipient_id=transaction.recipient.id,
            coins=transaction.coins,
        )

        self._session.add(transaction_db)

    async def update_user(self, user: User) -> None:
        stmt = update(UserDB).where(UserDB.id == user.id).values(
            username=user.username,
            password=user.password,
            coins=user.coins,
        )

        await self._session.execute(stmt)

    @staticmethod
    def _build_user(user_db: UserDB) -> User:
        return User(
            id=user_db.id,
            username=user_db.username,
            password=user_db.password,
            coins=user_db.coins,
        )


class SQLAlchemyUserUnitOfWork(UserUnitOfWork):
    def __init__(self):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()
        self.user_repository = SQLAlchemyUserRepository(self.session)
        return self

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
