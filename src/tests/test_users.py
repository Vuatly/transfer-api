import pytest

from src.domain.requests import UserRegisterRequest, UserLoginRequest
from src.domain.responses import ResponseType
from src.domain.usecases.user_login import UserLoginUseCase
from src.domain.usecases.user_register import UserRegisterUseCase
from src.tests.conftest import build_user


def test_user_eq():
    user1 = build_user()
    user2 = build_user()
    user3 = build_user()
    user2.id = user1.id

    assert user1 == user2
    assert user1 != user3


@pytest.mark.asyncio
async def test_user_register_success(memory_user_uow):
    usecase = UserRegisterUseCase(memory_user_uow)
    request = UserRegisterRequest(username="test", password="test")

    assert len(memory_user_uow.user_repository.users) == 0

    response = await usecase.execute(request)

    assert response.type == ResponseType.SUCCESS
    assert response.message == "OK"
    assert len(memory_user_uow.user_repository.users) == 1


@pytest.mark.asyncio
async def test_user_login_success(memory_user_uow):
    memory_user_uow.user_repository.users.append(build_user())
    request = UserLoginRequest(username="test", password="test")

    usecase = UserLoginUseCase(memory_user_uow)
    response = await usecase.execute(request)

    assert response.type == ResponseType.SUCCESS


@pytest.mark.asyncio
async def test_user_login_failed(memory_user_uow):
    memory_user_uow.user_repository.users.append(build_user())
    request = UserLoginRequest(username="test", password="fail")

    usecase = UserLoginUseCase(memory_user_uow)
    response = await usecase.execute(request)

    assert response.type == ResponseType.INVALID_PARAMETERS
