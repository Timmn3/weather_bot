from __future__ import annotations
from pydantic import BaseModel

class WeatherReport(BaseModel):
    """Данные о погоде в унифицированном виде."""
    city: str
    description: str
    temp: float
    wind_speed: float
