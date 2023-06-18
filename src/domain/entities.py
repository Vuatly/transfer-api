from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: uuid.UUID
    username: str
    password: str
    coins: int

    def __eq__(self, other: "User") -> bool:
        if not isinstance(other, User):
            return False

        return self.id == other.id


@dataclass(slots=True)
class Transaction:
    id: uuid.UUID
    sender: User
    recipient: User
    coins: int
