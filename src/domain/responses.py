from dataclasses import dataclass
from enum import Enum


class ResponseType(str, Enum):
    SUCCESS = "SUCCESS"
    INVALID_PARAMETERS = "INVALID_PARAMETERS"


@dataclass(slots=True, frozen=True)
class UserRegisterResponse:
    message: str
    type: ResponseType


@dataclass(slots=True, frozen=True)
class UserLoginResponse:
    message: str
    type: ResponseType


@dataclass(slots=True, frozen=True)
class TransferCoinsResponse:
    message: str
    type: ResponseType
