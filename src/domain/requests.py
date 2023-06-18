from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class UserRegisterRequest:
    username: str
    password: str


@dataclass(slots=True, frozen=True)
class UserLoginRequest:
    username: str
    password: str


@dataclass(slots=True, frozen=True)
class TransferCoinsRequest:
    from_id: UUID
    to_username: str
    coins: int
