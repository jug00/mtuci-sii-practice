from dishka import make_async_container

from .providers import YoloProvider

__all__ = ["container"]

container = make_async_container(YoloProvider())
