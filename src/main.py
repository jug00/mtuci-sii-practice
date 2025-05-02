from pathlib import Path

from dishka.integrations.litestar import setup_dishka
from litestar import Litestar, Router, Controller, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.static_files import StaticFilesConfig
from litestar.response import Template
from litestar.template import TemplateConfig

from apps.routers import route_handlers
from di import container
from src.db.database import init_db


class IndexController(Controller):
    @get(path="/", sync_to_thread=False)
    def index(self) -> Template:
        return Template(template_name="index.html", context={})

main_router = Router(
    path="api/",
    route_handlers=route_handlers,
)
swagger_plugin = SwaggerRenderPlugin(version="5.1.3", path="/swagger")


app = Litestar(
    route_handlers=[IndexController, main_router],
    openapi_config=OpenAPIConfig(title="Practice", version="1.0.0", render_plugins=[swagger_plugin]),
    debug=True,
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
    static_files_config=[
        StaticFilesConfig(path="/static", directories=["static"], html_mode=False)
    ],
)

init_db()
setup_dishka(container=container, app=app)