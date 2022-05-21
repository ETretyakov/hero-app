from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.core.models import StatusMessage
from app.heroes.crud import HeroesCRUD
from app.heroes.dependencies import get_heroes_crud
from app.heroes.models import HeroCreate, HeroPatch, HeroRead

router = APIRouter()


@router.post(
    "",
    response_model=HeroRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_hero(
        data: HeroCreate,
        heroes: HeroesCRUD = Depends(get_heroes_crud)
):
    hero = await heroes.create(data=data)

    return hero


@router.get(
    "/{hero_id}",
    response_model=HeroRead,
    status_code=http_status.HTTP_200_OK
)
async def get_hero_by_uuid(
        hero_id: str,
        heroes: HeroesCRUD = Depends(get_heroes_crud)
):
    hero = await heroes.get(hero_id=hero_id)

    return hero


@router.patch(
    "/{hero_id}",
    response_model=HeroRead,
    status_code=http_status.HTTP_200_OK
)
async def patch_hero_by_uuid(
        hero_id: str,
        data: HeroPatch,
        heroes: HeroesCRUD = Depends(get_heroes_crud)
):
    hero = await heroes.patch(hero_id=hero_id, data=data)

    return hero


@router.delete(
    "/{hero_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_hero_by_uuid(
        hero_id: str,
        heroes: HeroesCRUD = Depends(get_heroes_crud)
):
    status = await heroes.delete(hero_id=hero_id)

    return {"status": status, "message": "The hero has been deleted!"}
