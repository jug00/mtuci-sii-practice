import base64
import io
from typing import TYPE_CHECKING, Sequence

import cv2
import pandas as pd
from PIL import Image
from sqlmodel import Session, select

from . import models
from src.apps.analyse.tables import History
from ...db.database import save, engine

if TYPE_CHECKING:
    from ultralytics import YOLO


class AnalyseService:
    @staticmethod
    def predict(img_bytes: bytes, model: "YOLO") -> models.AnalyseResult:
        image = Image.open(io.BytesIO(img_bytes))
        results = model.predict(
            source=image,
            classes=[
                28,
            ],
            verbose=False,
        )
        annotated = results[0].plot()
        _, buffer = cv2.imencode(".jpg", annotated)

        b64_img = base64.b64encode(buffer).decode("utf-8")
        count = len(results[0])
        time_elapsed = sum(results[0].speed.values())

        record = History(
            count=count,
            time_elapsed=time_elapsed,
        )
        save(record)

        return models.AnalyseResult(
            count=count,
            time_elapsed=time_elapsed,
            processed_image=f"data:image/jpeg;base64,{b64_img}",
        )

    @staticmethod
    async def generate_excel_report() -> bytes:
        """Возвращает содержимое Excel-файла в виде байтов."""
        with Session(engine) as session:
            records = session.exec(select(History)).all()
        # Собираем словари для DataFrame
        rows = []
        for r in records:
            row = {
                "Время": r.timestamp.isoformat(),
                "Количество чемоданов": r.count,
                "Время выполнения (мс)": r.time_elapsed,
            }
            rows.append(row)
        df = pd.DataFrame(rows)
        stream = io.BytesIO()
        with pd.ExcelWriter(stream, engine="openpyxl") as writer: #type: ignore
            df.to_excel(writer, index=False, sheet_name="History")
        return stream.getvalue()

    @staticmethod
    async def fetch_history_records() -> Sequence[History]:
        with Session(engine) as session:
            return session.exec(select(History).order_by(History.id.desc())).all() #type: ignore
