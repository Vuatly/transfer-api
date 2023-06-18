import uuid

from src.domain.entities import User
from src.domain.repository import UserUnitOfWork
from src.domain.requests import UserRegisterRequest
from src.domain.responses import UserRegisterResponse, ResponseType
from src.pkg import security


class UserRegisterUseCase:
    def __init__(
        self,
        user_uow: UserUnitOfWork,
    ):
        self._user_uow = user_uow

    async def execute(self, data: UserRegisterRequest) -> UserRegisterResponse:
        user = User(
            id=uuid.uuid4(),
            username=data.username,
            password=security.hash_password(data.password),
            coins=100,
        )

        async with self._user_uow:
            await self._user_uow.user_repository.create(user)
            await self._user_uow.commit()

        return UserRegisterResponse(message="OK", type=ResponseType.SUCCESS)
