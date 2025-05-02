from dishka import Provider, provide, Scope
from ultralytics import YOLO


class YoloProvider(Provider):
    def __init__(self):
        super().__init__(scope=Scope.APP)
        self._yolo_model = YOLO("models/yolo11m.pt", verbose=False)

    @provide(scope=Scope.APP)
    def get_model(self) -> YOLO:
        return self._yolo_model