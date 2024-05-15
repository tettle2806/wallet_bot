from aiogram.fsm.state import StatesGroup, State


class ConversionState(StatesGroup):
    password = State()
    currency_pair = State()
    pair_well = State()
    quantity = State()
    wallet_sender = State()
    wallet_receive = State()
    accept = State()
