from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError

from src.api import factory
from src.api.codes import STATUS_CODES
from src.domain.requests import UserRegisterRequest, UserLoginRequest
from src.domain.usecases.user_login import UserLoginUseCase
from src.domain.usecases.user_register import UserRegisterUseCase

router = APIRouter(prefix="/users", tags=["users"])


class UserRegister(BaseModel):
    username: str = Field(..., min_length=4, max_length=32)
    password: str


class UserLogin(BaseModel):
    username: str = Field(..., min_length=4, max_length=32)
    password: str


@router.post(
    "/register",
    status_code=200,
    responses={
        200: {
            "description": "User created",
            "content": {
                "application/json": {
                    "example": {"message": "OK"},
                }
            },
        },
        400: {
            "description": "Duplicate user",
            "content": {
                "application/json": {
                    "example": {"message": "User with this username already exists."},
                }
            },
        },
    }
)
async def user_register(
    data: UserRegister,
    usecase: UserRegisterUseCase = Depends(factory.get_user_register_usecase),
):
    try:
        response = await usecase.execute(UserRegisterRequest(**data.dict()))
    except IntegrityError as e:
        logger.debug(e)
        return JSONResponse(
            status_code=400,
            content={"message": "User with this username already exists."},
        )

    return JSONResponse(
        status_code=STATUS_CODES[response.type],
        content={"message": response.message},
    )


@router.post(
    "/login",
    status_code=200,
    responses={
        200: {
            "description": "Get token",
            "content": {
                "application/json": {
                    "example": {
                        "token": "eyJhbGci0iJIUzI1NiIsIn5.eyJzdWIi0iIxMiMONTY30D"
                                 "kwIiwibmFtZ2NpYWwi0nRydWV9.4pcPMD0901PSzdI1AVTmud2fU4",
                    },
                }
            }
        },
        400: {
            "description": "Invalid username or password",
            "content": {
                "application/json": {
                    "example": {"message": "Invalid username or passwrd"},
                }
            }
        },
    }
)
async def login_user(
    data: UserLogin,
    usecase: UserLoginUseCase = Depends(factory.get_user_login_usecase),
):
    response = await usecase.execute(UserLoginRequest(data.username, data.password))

    return JSONResponse(
        content={"token": response.message},
        status_code=STATUS_CODES[response.type],
    )
