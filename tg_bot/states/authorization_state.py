from aiogram.fsm.state import StatesGroup, State


class AuthorizationState(StatesGroup):
    check_password = State()
    set_password = State()