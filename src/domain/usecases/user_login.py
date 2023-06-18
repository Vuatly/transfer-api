from src.domain.repository import UserUnitOfWork
from src.domain.requests import UserLoginRequest
from src.domain.responses import UserLoginResponse, ResponseType
from src.pkg import security


class UserLoginUseCase:
    def __init__(self, user_uow: UserUnitOfWork):
        self._user_uow = user_uow

    async def execute(self, data: UserLoginRequest) -> UserLoginResponse:
        async with self._user_uow:
            user = await self._user_uow.user_repository.get_by_username(data.username)

        if not user or not security.verify_password(data.password, user.password):
            return UserLoginResponse(
                message="Invalid username or password",
                type=ResponseType.INVALID_PARAMETERS,
            )

        token = security.create_access_token(data={"user_id": str(user.id)})

        return UserLoginResponse(message=token, type=ResponseType.SUCCESS)
