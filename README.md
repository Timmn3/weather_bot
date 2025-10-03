# Weather Telegram Bot

Простой Telegram-бот для получения текущей погоды по городу или геолокации.

## Быстрый старт
1) Python 3.12 установлен.
2) Установите зависимости:
```bash
pip install -r requirements.txt
```
3) Создайте файл `.env` (можно скопировать из `.env.example`) и заполните значения (см. раздел ENV).
4) Запустите бота:
```bash
python -m main
```

## ENV
- `BOT_TOKEN` — токен Telegram-бота
- `WEATHER_API_KEY` — API-ключ OpenWeather (Current Weather Data)
- `DEFAULT_UNITS` — `metric` (°C, м/с) или `imperial` (°F, mph). По умолчанию `metric`
- `OPENWEATHER_LANG` — язык описания погоды, например `ru`

Пример `.env`:
```
BOT_TOKEN=123456:replace_me
WEATHER_API_KEY=replace_me
DEFAULT_UNITS=metric
OPENWEATHER_LANG=ru
```

## Команды
- `/start` — краткая справка и кнопка отправки геолокации
- `/weather <город>` — текущая погода. Примеры: `/weather Moscow`, `/weather Paris,fr`
- `/celsius` — переключить вывод в °C
- `/fahrenheit` — переключить вывод в °F

Также поддерживается:
- Отправка геолокации кнопкой «Отправить локацию»
- Ручной ввод координат сообщением: `55.7558, 37.6176`

## Архитектура
- `bot/handlers.py` — хендлеры команд, геолокации и координат
- `bot/keyboards.py` — клавиатуры (кнопка для локации)
- `weather/api_client.py` — клиент OpenWeather (HTTP-запросы)
- `weather/models.py` — модель `WeatherReport`
- `weather/cache.py` — простой in-memory кэш (TTL 5 минут) и хранение единиц на пользователя
- `weather/formatting.py` — форматирование ответа
- `config.py` — настройки из `.env`
- `main.py` — точка входа 

## Тесты
Запуск:
```bash
pytest -q
```
Покрытие:
- парсинг ответа API (`tests/test_api_parse.py`)
- форматирование сообщения (`tests/test_formatting.py`)

## Примечания
- Для ключа OpenWeather используйте «Current Weather Data» (endpoint `/data/2.5/weather`).
- Если при первых запросах получаете `401`, проверьте активацию ключа в кабинете OpenWeather и подтверждение e-mail.

## Установка из GitHub (git clone)
```bash
git clone https://github.com/Timmn3/weather_bot.git
cd weather_bot

# (опционально) создать venv
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt

# Настроить переменные окружения в .env
cp .env.example .env  # если есть .env.example
# Открыть .env и указать:
# BOT_TOKEN=...
# WEATHER_API_KEY=...
# DEFAULT_UNITS=metric
# OPENWEATHER_LANG=ru

# Запуск
python -m main
```

##  Запуск через Docker
1) Сборка образа

```bash
docker build -t weather-bot .
```

2) Запуск контейнера (используя .env)

.env не копируется в образ — передаём при запуске:
```bash
docker run -d \
  --name weather-bot \
  --env-file ./.env \
  --restart unless-stopped \
  weather-bot
```
3) Логи
```bash
docker logs -f weather-bot
```