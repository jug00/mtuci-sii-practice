from dataclasses import dataclass

@dataclass(frozen=True)
class AnalyseResult:
    count: int
    time_elapsed: float
    processed_image: str