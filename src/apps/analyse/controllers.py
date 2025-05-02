from typing import Annotated, Sequence

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post, Router, get, Response
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from ultralytics import YOLO

from . import models

from src.apps.analyse.services import AnalyseService
from src.apps.analyse.tables import History


class AnalyseController(Controller):
    path = "/analyse"
    tags = ["Analyse"]

    @post(path="/predict-image", media_type=None)
    @inject
    async def predict_image(
        self,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        model_yolo: FromDishka[YOLO]
    ) -> models.AnalyseResult:
        img_bytes = await data.read()
        return AnalyseService.predict(img_bytes, model_yolo)

    @get("/history/report")
    async def download_report(self) -> Response:
        data = await AnalyseService.generate_excel_report()
        return Response(
            content=data,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=history_report.xlsx",
                "Cache-Control": "no-cache",
            },
        )

    @get(path="/history")
    async def get_history(self) -> Response[Sequence[History]]:
        records = await AnalyseService.fetch_history_records()
        return Response(
            content=records,
            media_type="application/json",
        )

analyse_router = Router(
    path="/",
    route_handlers=[
        AnalyseController,
    ],
)
