from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from tg_bot.data.config import ADMIN_ID, ADMINS
from tg_bot.data.loader import db
from tg_bot.states.add_del_state import NewUser
admin_router = Router()


@admin_router.message(F.text == '/add')
async def add_user(message: types.Message, state: FSMContext):

    if str(message.chat.id) in ADMINS:
        await message.answer('Отправьте ID нового пользователя\nID можете посмотреть через https://t.me/my_id_bot')
        await state.set_state(NewUser.add_id)
    else:
        await message.answer('У вас нет доступа')


@admin_router.message(NewUser.add_id)
async def save_new_user_in_db(message: types.Message, state: FSMContext):
    new_user_id = message.text
    await state.update_data(id=new_user_id)
    if db.get_user_by_id(new_user_id):
        await message.answer('Пользователь уже добавлен')
        await state.clear()
    else:
        # добавление нового пользователя в бд
        info = await state.get_data()
        db.insert_user(new_user_id)
        await message.answer('Пользователь добавлен')
        await state.clear()


@admin_router.message(F.text == '/delete')
async def delete_user(message: types.Message, state: FSMContext):
    if str(message.chat.id) in ADMINS:
        await message.answer('Отправьте ID пользователя\nID можете посмотреть через https://t.me/my_id_bot')
        await state.set_state(NewUser.del_id)
    else:
        await message.answer('У вас нет доступа')


@admin_router.message(NewUser.del_id)
async def delete_user_db(message: types.Message, state: FSMContext):
    new_user_id = message.text
    await state.set_state(NewUser.del_id)
    if db.get_user_by_id(new_user_id):
        db.delete_user(new_user_id)
        await message.answer('Пользователь удален')
        await state.clear()
    else:
        await message.answer('Такого пользователя нет')
        await state.clear()