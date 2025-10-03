import pytest
from weather.api_client import OpenWeatherClient
from weather.models import WeatherReport

@pytest.mark.asyncio
async def test_to_report_parsing():
    client = OpenWeatherClient(api_key="test", lang="ru")
    # упрощённый фрагмент ответа OpenWeather
    data = {
        "name": "Moscow",
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 12.34},
        "wind": {"speed": 3.21},
    }
    report = client._to_report(data)
    assert isinstance(report, WeatherReport)
    assert report.city == "Moscow"
    assert report.description == "clear sky"
    assert report.temp == pytest.approx(12.34, rel=1e-3)
    assert report.wind_speed == pytest.approx(3.21, rel=1e-3)
