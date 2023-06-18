from uuid import UUID

from sqlalchemy import select

from src.infra.models import UserDB
from src.pkg.alchemy import session_factory


async def get_user_coins(uid: UUID) -> dict[str, int]:
    async with session_factory() as session:
        stmt = select(UserDB).where(UserDB.id == uid)
        result = await session.execute(stmt)

        user_db = result.scalars().one()
        return {"coins": user_db.coins}
