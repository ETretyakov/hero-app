from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.heroes.crud import HeroesCRUD


async def get_heroes_crud(
        session: AsyncSession = Depends(get_async_session)
) -> HeroesCRUD:
    return HeroesCRUD(session=session)
