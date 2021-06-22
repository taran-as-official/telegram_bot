import logging
from bot.postgres import PostgreSQL

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT, ADMIN_ID)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
db = PostgreSQL()






@dp.callback_query_handler(lambda c: c.data == 'www_game')
async def process_callback_www_game(callback_query: types.CallbackQuery):

    await callback_query.answer('Будем играть в что где когда!')


@dp.message_handler(commands=['start'])
async def start_fnc(message: types.Message):
    # получаем информацию о пользователе
    user = db.get_user_info(message.from_user.id)

    #если пользователя не существует в БД, то добавим его
    if not(user):
        db.add_user_info(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)

    # инициируем кнопки
    www_game = types.InlineKeyboardButton('Что? Где? Когда?', callback_data='www_game')
    inline_games = types.InlineKeyboardMarkup().add(www_game)
    logging.info(f'Получено сообщение от {message.from_user}')
    await message.answer(f'Привет, во что будем играть?', reply_markup = inline_games)

    if message.from_user.id != ADMIN_ID:
        await bot.send_message(ADMIN_ID, f'{message.from_user.full_name} присоединился к боту')


@dp.message_handler()
async def echo(message: types.Message):

	logging.warning(str(message))
	await bot.send_message(message.chat.id, message.text)




async def on_startup(dp):
    logging.warning(
        'Установка Вебхука')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Выключение Вебхука')


logging.info(f'САМЫЙ КОНЕЦ ПРОГРАММЫ')

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
