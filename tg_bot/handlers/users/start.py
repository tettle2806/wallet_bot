import hashlib

from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, ReplyKeyboardRemove

from tg_bot.data.loader import bot, db
from tg_bot.keyboards.reply import main_kb
from tg_bot.states.authorization_state import AuthorizationState

start_router = Router()


@start_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if db.get_user_by_id(chat_id):
        if db.select_password(chat_id)[0]:
            await message.answer('Введите пароль:', reply_markup=ReplyKeyboardRemove())
            await state.set_state(AuthorizationState.check_password)
        else:
            await message.answer('Установите пароль', reply_markup=ReplyKeyboardRemove())
            await state.set_state(AuthorizationState.set_password)
    else:
        await message.answer('Доступ запрещен')


@start_router.message(AuthorizationState.check_password)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if db.select_password(chat_id)[0] == hashlib.sha256(message.text.encode('utf-8')).hexdigest():
        await message.answer('Авторизация пройдена', reply_markup=main_kb())
        await state.clear()
    else:
        await message.answer('Не верный пароль, введите правильный пароль')
        await state.set_state(AuthorizationState.check_password)


@start_router.message(AuthorizationState.set_password)
async def set_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    db.insert_password(telegram_id=chat_id, password=hashlib.sha256(message.text.encode('utf-8')).hexdigest())
    await message.answer('Пароль установлен', reply_markup=main_kb())
    await state.clear()
