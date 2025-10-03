from aiogram.fsm.state import StatesGroup, State

class WeatherStates(StatesGroup):
    """Состояния FSM для получения города."""
    waiting_for_city = State()
