import logging

from aiogram import Dispatcher

from data.config import admins
from keyboards.default import def_kb


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе", reply_markup=def_kb)

        except Exception as err:
            logging.exception(err)
