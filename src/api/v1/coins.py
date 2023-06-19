from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from src.api import queries, factory
from src.api.codes import STATUS_CODES
from src.domain.requests import TransferCoinsRequest
from src.domain.usecases.transfer_coins import TransferCoinsUseCase
from src.pkg import security
from src.pkg.security import JWTPayload

router = APIRouter(prefix="/coins", tags=["coins"])


class TransferCoins(BaseModel):
    recipient_username: str = Field(
        ...,
        min_length=4,
        max_length=32,
        description="Username of recipient"
    )
    coins: int = Field(
        ...,
        ge=1,
        description="Coins to transfer",
    )


@router.get("/balance", status_code=200)
async def get_user_coins_balance(payload: JWTPayload = Depends(security.auth_required)):
    return await queries.get_user_coins(UUID(payload["user_id"]))


@router.post("/transfer", status_code=200)
async def transfer_coins(
    data: TransferCoins,
    payload: JWTPayload = Depends(security.auth_required),
    usecase: TransferCoinsUseCase = Depends(factory.get_transfer_coins_usecase),
):
    response = await usecase.execute(
        TransferCoinsRequest(
            from_id=UUID(payload["user_id"]),
            to_username=data.recipient_username,
            coins=data.coins,
        )
    )

    return JSONResponse(
        status_code=STATUS_CODES[response.type],
        content={"message": response.message},
    )
