import hashlib

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.data.loader import db
from tg_bot.keyboards.reply import back_btn, main_kb, setting_btn, accept_transactions
from tg_bot.states.setting_state import Setting

settings_router = Router()


@settings_router.message(F.text == '⚙️Настройки')
async def settings(message: Message, state: FSMContext):
    await message.answer('Введите пароль', reply_markup=back_btn())
    await state.set_state(Setting.password)


@settings_router.message(Setting.password)
async def password_setting_state(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=main_kb())
        await state.clear()
    else:
        if db.select_password(chat_id)[0] == hashlib.sha256(message.text.encode('utf-8')).hexdigest():
            await message.answer('Выберите действие', reply_markup=setting_btn())
            await state.set_state(Setting.step1)
        else:
            await message.answer('Не верный пароль')
            await state.set_state(Setting.password)


@settings_router.message(Setting.step1)
async def main_setting(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '🗑️ Очистить транзакции':
        await message.answer('Подтвердите действие', reply_markup=accept_transactions())
        await state.set_state(Setting.delete_tables)
    elif message.text == '🔙 Назад':
        await message.answer('Главное меню', reply_markup=main_kb())
    elif message.text == '☢️ Изменить пароль':
        await message.answer('Введите нынешний пароль',reply_markup=back_btn())
        await state.set_state(Setting.set_pass)
    else:
        await message.answer('Выберите действие')
        await state.set_state(Setting.step1)


@settings_router.message(Setting.delete_tables)
async def drop_transaction_table(message: Message, state: FSMContext):
    if message.text == 'Подтвердить':
        db.drop_transactions()
        db.create_transactions()
        await message.answer('Операция прошла успешно', reply_markup=setting_btn())
        await state.set_state(Setting.step1)
    elif message.text == 'Отменить':
        await message.answer('Действие отменено', reply_markup=setting_btn())
        await state.set_state(Setting.step1)
    else:
        await message.answer('Подтвердите или отмените действие', reply_markup=accept_transactions())
        await state.set_state(Setting.delete_tables)


@settings_router.message(Setting.set_pass)
async def set_pass_state(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=setting_btn())
        await state.set_state(Setting.step1)
    else:
        if db.select_password(chat_id)[0] == hashlib.sha256(message.text.encode('utf-8')).hexdigest():
            await message.answer('Введите новый пароль', reply_markup=back_btn())
            await state.set_state(Setting.new_password)
        else:
            await message.answer('Не верный пароль')
            await state.set_state(Setting.set_pass)


@settings_router.message(Setting.new_password)
async def set_new_pass_state(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '🔙 Назад':
        await message.answer('Действие отменено', reply_markup=setting_btn())
        await state.set_state(Setting.step1)
    else:
        new_pass = hashlib.sha256(message.text.encode('utf-8')).hexdigest()
        db.insert_password(telegram_id=chat_id, password=new_pass)
        await message.answer('Новый пароль установлен', reply_markup=setting_btn())
        await state.set_state(Setting.step1)