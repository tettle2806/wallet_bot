from aiogram.fsm.state import StatesGroup, State


class AnalyticsState(StatesGroup):
    password = State()
    step1 = State()
    balance = State()
    income = State()
    expense = State()
    transaction = State()
