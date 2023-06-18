import uuid

from src.domain.entities import Transaction
from src.domain.repository import UserUnitOfWork
from src.domain.requests import TransferCoinsRequest
from src.domain.responses import TransferCoinsResponse, ResponseType


class TransferCoinsUseCase:
    def __init__(self, user_uow: UserUnitOfWork):
        self._user_uow = user_uow

    async def execute(self, data: TransferCoinsRequest):
        async with self._user_uow:
            from_user = await self._user_uow.user_repository.get_by_id(
                data.from_id,
                for_update=True,
            )

            if not from_user:
                return TransferCoinsResponse(
                    message="Invalid sender",
                    type=ResponseType.INVALID_PARAMETERS,
                )

            to_user = await self._user_uow.user_repository.get_by_username(
                data.to_username,
                for_update=True,
            )

            if not to_user or from_user == to_user:
                return TransferCoinsResponse(
                    message="Invalid recipient",
                    type=ResponseType.INVALID_PARAMETERS,
                )

            if from_user.coins < data.coins:
                return TransferCoinsResponse(
                    message="Not enough money",
                    type=ResponseType.INVALID_PARAMETERS,
                )

            from_user.coins -= data.coins
            to_user.coins += data.coins

            await self._user_uow.user_repository.update_user(from_user)
            await self._user_uow.user_repository.update_user(to_user)

            transaction = Transaction(
                id=uuid.uuid4(),
                sender=from_user,
                recipient=to_user,
                coins=data.coins,
            )

            await self._user_uow.user_repository.create_transaction(transaction)

            await self._user_uow.commit()

        return TransferCoinsResponse(
            message="OK",
            type=ResponseType.SUCCESS,
        )

