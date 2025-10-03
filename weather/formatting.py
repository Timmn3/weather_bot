from weather.models import WeatherReport

def format_weather_report(report: WeatherReport, units: str) -> str:
    """Форматирование ответа для пользователя."""
    t_unit = "°C" if units == "metric" else "°F"
    w_unit = "м/с" if units == "metric" else "mph"
    text = (
        f"<b>{report.city}</b>\n"
        f"{report.description.capitalize()}\n"
        f"Температура: <b>{round(report.temp, 1)} {t_unit}</b>\n"
        f"Ветер: {round(report.wind_speed, 1)} {w_unit}"
    )
    return text
