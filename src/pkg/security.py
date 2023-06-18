from datetime import timedelta, datetime
from typing import TypedDict

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from loguru import logger
from passlib.context import CryptContext

from src import conf

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTPayload(TypedDict):
    user_id: str
    exp: int


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_str: str) -> bool:
    return pwd_context.verify(password, hash_str)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, conf.JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def auth_required(
    auth: HTTPAuthorizationCredentials = Security(
        HTTPBearer(auto_error=False)
    )
) -> JWTPayload:
    if not auth:
        raise HTTPException(status_code=401, detail="Token is not provided")

    return _decode_token(auth.credentials)


def _decode_token(token: str) -> JWTPayload:
    try:
        payload = jwt.decode(
            token,
            conf.JWT_SECRET_KEY,
            algorithms=["HS256"],
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        logger.debug(e)
        raise HTTPException(
            status_code=401,
            detail="Signature has expired",
        )
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=401, detail="Invalid token")
