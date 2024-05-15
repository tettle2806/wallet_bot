from aiogram.fsm.state import StatesGroup, State


class NewExpenses(StatesGroup):
    category = State()
    password = State()
    uzs_usd = State()
    sub_category = State()
    quantity = State()
    cart_name = State()
    description = State()
    accept = State()
