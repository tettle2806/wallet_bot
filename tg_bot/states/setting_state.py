from aiogram.fsm.state import StatesGroup, State


class Setting(StatesGroup):
    password = State()
    step1 = State()
    delete_tables = State()
    set_pass = State()
    new_password = State()
