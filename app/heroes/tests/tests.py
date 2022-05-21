import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.heroes.models import Hero


@pytest.mark.asyncio
async def test_create_hero(
        async_client: AsyncClient,
        async_session: AsyncSession,
        test_data: dict
):
    payload = test_data["case_create"]["payload"]
    response = await async_client.post("/heroes", json=payload,)

    assert response.status_code == 201

    got = response.json()
    want = test_data["case_create"]["want"]

    for k, v in want.items():
        assert got[k] == v

    statement = select(Hero).where(Hero.uuid == got["uuid"])
    results = await async_session.execute(statement=statement)
    hero = results.scalar_one()

    for k, v in want.items():
        assert getattr(hero, k) == v


@pytest.mark.asyncio
async def test_get_hero(
        async_client: AsyncClient,
        async_session: AsyncSession,
        test_data: dict
):
    hero_data = test_data["initial_data"]["hero"]
    statement = insert(Hero).values(hero_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.get(f"/heroes/{hero_data['uuid']}")
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_get"]["want"]

    for k, v in want.items():
        assert got[k] == v


@pytest.mark.asyncio
async def test_patch_hero(
        async_client: AsyncClient,
        async_session: AsyncSession,
        test_data: dict
):
    hero_data = test_data["initial_data"]["hero"]
    statement = insert(Hero).values(hero_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    payload = test_data["case_patch"]["payload"]
    response = await async_client.patch(
        f"/heroes/{hero_data['uuid']}",
        json=payload
    )
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_patch"]["want"]

    for k, v in want.items():
        assert got[k] == v


@pytest.mark.asyncio
async def test_delete_hero(
        async_client: AsyncClient,
        async_session: AsyncSession,
        test_data: dict
):
    hero_data = test_data["initial_data"]["hero"]
    statement = insert(Hero).values(hero_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.delete(f"/heroes/{hero_data['uuid']}")
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_delete"]["want"]

    for k, v in want.items():
        assert got[k] == v

    statement = select(
        Hero
    ).where(
        Hero.uuid == hero_data["uuid"]
    )
    results = await async_session.execute(statement=statement)
    hero = results.scalar_one_or_none()

    assert hero is None
