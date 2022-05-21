from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.heroes.models import Hero, HeroCreate, HeroPatch


class HeroesCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: HeroCreate) -> Hero:
        values = data.dict()

        hero = Hero(**values)
        self.session.add(hero)
        await self.session.commit()
        await self.session.refresh(hero)

        return hero

    async def get(self, hero_id: str | UUID) -> Hero:
        statement = select(
            Hero
        ).where(
            Hero.uuid == hero_id
        )
        results = await self.session.execute(statement=statement)
        hero = results.scalar_one_or_none()  # type: Hero | None

        if hero is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The hero hasn't been found!"
            )

        return hero

    async def patch(self, hero_id: str | UUID, data: HeroPatch) -> Hero:
        hero = await self.get(hero_id=hero_id)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(hero, k, v)

        self.session.add(hero)
        await self.session.commit()
        await self.session.refresh(hero)

        return hero

    async def delete(self, hero_id: str | UUID) -> bool:
        statement = delete(
            Hero
        ).where(
            Hero.uuid == hero_id
        )

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
