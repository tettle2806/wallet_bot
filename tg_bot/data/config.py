import os

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
ADMIN_ID = str(os.getenv("ADMIN_ID"))
ADMINS = str(os.getenv("ADMINS"))


def root_path() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent.parent  # Тут выход в корень проекта


TRANSACTION_PATH = os.path.join(root_path(), 'tg_bot\\files\\transactions.xlsx')
INCOME_PATH = os.path.join(root_path(), 'tg_bot\\files\\income.xlsx')
EXPENSES_PATH = os.path.join(root_path(), 'tg_bot\\files\\expenses.xlsx')
BALANCES_PATH = os.path.join(root_path(), 'tg_bot\\files\\balances.xlsx')
# D:\Портфолио\django Projects\acc_bot\tg_bot\handlers\users\acc.xlsx
DB_PATH = os.path.join(root_path(), 'tg_bot\\acc.db')


# Сделать проверку по ID
async def set_commands(bot: Bot):
    commands_for_admin = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='add',
            description='Добавление пользователя'
        ),
        BotCommand(
            command='delete',
            description='Удаление пользователя'
        )
    ]
    await bot.set_my_commands(commands_for_admin, BotCommandScopeChat(chat_id=ADMIN_ID))

    commands_for_user = [
        BotCommand(
            command='start',
            description='Начало работы'
        )
    ]
    await bot.set_my_commands(commands_for_user, BotCommandScopeDefault())
