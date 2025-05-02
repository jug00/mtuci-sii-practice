from sqlmodel import SQLModel, Field
from datetime import datetime

class History(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    count: int
    time_elapsed: float

