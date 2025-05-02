from typing import TYPE_CHECKING

from litestar import Router

from .analyse.controllers import analyse_router

if TYPE_CHECKING:
    from litestar.types import ControllerRouterHandler

route_handlers: list["ControllerRouterHandler"] = [
    Router(
        path="v1",
        route_handlers=[
            analyse_router,
        ],
    ),
]