from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault
from tg_bot.data.config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage

from tg_bot.database.database import DataBase

storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)
db = DataBase()

