import uuid

import pytest

from src.domain.requests import TransferCoinsRequest
from src.domain.responses import ResponseType
from src.domain.usecases.transfer_money import TransferCoinsUseCase
from src.tests.conftest import build_user


@pytest.mark.asyncio
async def test_transfer_money_success(memory_user_uow):
    sender = build_user()
    recipient = build_user(username="test2")
    memory_user_uow.user_repository.users.extend([sender, recipient])

    request = TransferCoinsRequest(
        from_id=sender.id,
        to_username=recipient.username,
        coins=10,
    )

    assert len(memory_user_uow.user_repository.transactions) == 0

    usecase = TransferCoinsUseCase(memory_user_uow)
    response = await usecase.execute(request)

    assert response.type == ResponseType.SUCCESS
    assert response.message == "OK"
    assert sender.coins == 90
    assert recipient.coins == 110
    assert len(memory_user_uow.user_repository.transactions) == 1


@pytest.mark.asyncio
async def test_transfer_money_invalid_sender(memory_user_uow):
    recipient = build_user(username="test2")
    memory_user_uow.user_repository.users.append(recipient)

    request = TransferCoinsRequest(
        from_id=uuid.uuid4(),
        to_username=recipient.username,
        coins=10,
    )

    assert len(memory_user_uow.user_repository.transactions) == 0

    usecase = TransferCoinsUseCase(memory_user_uow)
    response = await usecase.execute(request)

    assert response.type == ResponseType.INVALID_PARAMETERS
    assert response.message == "Invalid sender"
    assert len(memory_user_uow.user_repository.transactions) == 0


@pytest.mark.asyncio
async def test_transfer_money_invalid_recipient(memory_user_uow):
    sender = build_user()
    memory_user_uow.user_repository.users.append(sender)

    request = TransferCoinsRequest(
        from_id=sender.id,
        to_username="test2",
        coins=10,
    )

    assert len(memory_user_uow.user_repository.transactions) == 0

    usecase = TransferCoinsUseCase(memory_user_uow)
    response = await usecase.execute(request)

    assert response.type == ResponseType.INVALID_PARAMETERS
    assert response.message == "Invalid recipient"
    assert len(memory_user_uow.user_repository.transactions) == 0


@pytest.mark.asyncio
async def test_transfer_money_not_enough_money(memory_user_uow):
    sender = build_user()
    recipient = build_user(username="test2")
    memory_user_uow.user_repository.users.extend([sender, recipient])

    request = TransferCoinsRequest(
        from_id=sender.id,
        to_username=recipient.username,
        coins=1000,
    )

    assert len(memory_user_uow.user_repository.transactions) == 0

    usecase = TransferCoinsUseCase(memory_user_uow)
    response = await usecase.execute(request)

    assert response.type == ResponseType.INVALID_PARAMETERS
    assert response.message == "Not enough money"
    assert len(memory_user_uow.user_repository.transactions) == 0
