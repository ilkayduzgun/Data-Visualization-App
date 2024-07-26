from pydantic import BaseModel
from typing import Optional

class sensor_data(BaseModel):
    temp: int
    pressure: int
    current: int
    error: bool
    timestamp: Optional[str] = None