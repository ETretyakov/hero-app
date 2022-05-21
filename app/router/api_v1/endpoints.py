from fastapi import APIRouter

from app.heroes.api import router as heroes_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (heroes_router, "heroes", "heroes"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
