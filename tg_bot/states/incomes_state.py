from aiogram.fsm.state import StatesGroup, State


class NewIncome(StatesGroup):
    category = State()
    password = State()
    uzs_usd = State()
    quantity = State()
    description = State()
    accept = State()
