from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.core.models import StatusMessage
from app.heroes.models import Hero, HeroCreate, HeroPatch, HeroRead
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("", response_model=HeroRead, status_code=http_status.HTTP_201_CREATED)
async def create_hero(
    data: HeroCreate, session: AsyncSession = Depends(get_async_session)
):
    hero = await Hero.create(data=data, session=session)

    return hero


@router.get("/{hero_id}", response_model=HeroRead, status_code=http_status.HTTP_200_OK)
async def get_hero_by_uuid(
    hero_id: str, session: AsyncSession = Depends(get_async_session)
):
    msg = "Hero Not Found"
    hero = await Hero.get(id=hero_id, session=session, msg=msg)
    return hero


@router.patch(
    "/{hero_id}", response_model=HeroRead, status_code=http_status.HTTP_200_OK
)
async def patch_hero_by_uuid(
    hero_id: str, data: HeroPatch, session: AsyncSession = Depends(get_async_session)
):
    hero = await Hero.patch(id=hero_id, data=data, session=session)
    return hero


@router.delete(
    "/{hero_id}", response_model=StatusMessage, status_code=http_status.HTTP_200_OK
)
async def delete_hero_by_uuid(
    hero_id: str, session: AsyncSession = Depends(get_async_session)
):
    status = await Hero.delete(id=hero_id, session=session)
    return {"status": status, "message": "The hero has been deleted!"}
