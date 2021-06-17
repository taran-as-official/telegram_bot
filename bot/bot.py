import logging
from bot.postgres import PostgreSQL

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
db = PostgreSQL()

@dp.message_handler(commands=['start', 'help'])
async def start_fnc(message: types.Message):
    logging.info(f'Получено сообщение от {message.from_user}')
    await bot.send_message(message.chat.id, 'Привет, далее все что напишешь вернется тебе как ЭХО!')
    if db.subscriber_exists(message.from_user.id):
        await bot.send_message(message.chat.id, 'Ты есть в базе!')
    else:
        await bot.send_message(message.chat.id, 'Тебя нет в базе!')


@dp.message_handler()
async def echo(message: types.Message):

	logging.warning(str(message))
	await bot.send_message(message.chat.id, message.text)
	

		

async def on_startup(dp):
    logging.warning(
        'Starting connection. \(Установка Вебхука\) ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection \(Выключение Вебхука\)')


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
