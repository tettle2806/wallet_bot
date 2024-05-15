from aiogram.fsm.state import StatesGroup, State


class NewUser(StatesGroup):
    add_id = State()
    del_id = State()
