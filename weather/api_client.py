import httpx
from typing import Any, Dict
from weather.models import WeatherReport

OPENWEATHER_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

class OpenWeatherClient:
    """Клиент для запросов к OpenWeather API."""
    def __init__(self, api_key: str, lang: str = "ru") -> None:
        self.api_key = api_key
        self.lang = lang

    async def _request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(OPENWEATHER_WEATHER_URL, params=params)
            # Пытаемся показать полезное сообщение об ошибке
            if r.status_code >= 400:
                try:
                    detail = r.json()
                except Exception:
                    detail = {"text": r.text}
                # Поднимем осмысленную ошибку (увидим cod/message)
                raise RuntimeError(f"OpenWeather error {r.status_code}: {detail}")
            return r.json()

    async def get_by_city(self, city: str, units: str = "metric") -> WeatherReport:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
            "lang": self.lang,
        }
        data = await self._request(params)
        return self._to_report(data)

    async def get_by_coords(self, lat: float, lon: float, units: str = "metric") -> WeatherReport:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": units,
            "lang": self.lang,
        }
        data = await self._request(params)
        return self._to_report(data)

    def _to_report(self, data: Dict[str, Any]) -> WeatherReport:
        """Преобразуем ответ OpenWeather в WeatherReport."""
        city = data.get("name") or "Unknown"
        description = (data.get("weather") or [{}])[0].get("description") or "—"
        temp = float(data.get("main", {}).get("temp"))
        wind = float(data.get("wind", {}).get("speed", 0.0))
        return WeatherReport(city=city, description=description, temp=temp, wind_speed=wind)
