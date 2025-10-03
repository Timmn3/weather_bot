from weather.models import WeatherReport
from weather.formatting import format_weather_report

def test_formatting_metric():
    rep = WeatherReport(city="Moscow", description="clear sky", temp=10.0, wind_speed=5.0)
    text = format_weather_report(rep, "metric")
    assert "°C" in text
    assert "м/с" in text
    assert "Moscow" in text
    assert "Clear sky" in text  # капитализация

def test_formatting_imperial():
    rep = WeatherReport(city="NYC", description="light rain", temp=50.0, wind_speed=7.0)
    text = format_weather_report(rep, "imperial")
    assert "°F" in text
    assert "mph" in text
    assert "NYC" in text
    assert "Light rain" in text
