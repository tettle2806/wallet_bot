import logging

from aiogram import Bot
import os
from dotenv import load_dotenv
from tg_bot.data.config import ADMIN_ID


async def admin_notify(bot: Bot):
    try:
        text = 'Бот запущен'
        await bot.send_message(chat_id=ADMIN_ID, text=text)
    except Exception as e:
        logging.error(e)

