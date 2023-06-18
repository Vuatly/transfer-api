from src.domain.usecases.transfer_money import TransferCoinsUseCase
from src.domain.usecases.user_login import UserLoginUseCase
from src.domain.usecases.user_register import UserRegisterUseCase
from src.infra.repository import SQLAlchemyUserUnitOfWork


def get_user_register_usecase() -> UserRegisterUseCase:
    user_uow = SQLAlchemyUserUnitOfWork()
    return UserRegisterUseCase(user_uow)


def get_user_login_usecase() -> UserLoginUseCase:
    user_uow = SQLAlchemyUserUnitOfWork()
    return UserLoginUseCase(user_uow)


def get_transfer_coins_usecase() -> TransferCoinsUseCase:
    user_uow = SQLAlchemyUserUnitOfWork()
    return TransferCoinsUseCase(user_uow)
