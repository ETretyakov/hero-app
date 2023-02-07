from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from app.core.models import TimestampModel, UUIDModel
from uuid import UUID
from sqlalchemy import delete, select
from fastapi import HTTPException
from fastapi import status as http_status


class ActiveRecord(UUIDModel, TimestampModel):
    @classmethod
    async def create(cls, data, session: AsyncSession):
        values = data.dict()

        obj = cls(**values)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

        return obj

    @classmethod
    async def get(cls, id: str | UUID, session: AsyncSession, msg: str = "Not Found"):
        statement = select(cls).where(cls.uuid == id)
        results = await session.execute(statement=statement)
        data = results.scalar_one_or_none()

        if data is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=msg,
            )

        return data

    @classmethod
    async def patch(
        cls, id: str | UUID, data, session: AsyncSession, msg: str = "Not Found"
    ):
        current = await cls.get(id=id, session=session)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(current, k, v)

        session.add(current)
        await session.commit()
        await session.refresh(current)

        return current

    @classmethod
    async def delete(cls, id: str | UUID, session: AsyncSession) -> bool:
        statement = delete(cls).where(cls.uuid == id)

        await session.execute(statement=statement)
        await session.commit()

        return True
