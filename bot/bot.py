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

user = None
logging.info(f'НАЧАЛО ПРОГРАММЫ')

some_var = 'default'
#инициализируем конпки
www_game = types.InlineKeyboardButton('Что? Где? Когда?', callback_data='www_game')
kwiz = types.InlineKeyboardButton('Квиз', callback_data='kwiz')
inline_games = types.InlineKeyboardMarkup().add(www_game,kwiz)


@dp.callback_query_handler(lambda c: c.data == 'www_game')
async def process_callback_www_game(callback_query: types.CallbackQuery):
    logging.info(f'Информация по юзеру что где когда: {user} из переменная some_var: {some_var}' )
    await callback_query.answer('Будем играть в что где когда!',True)


@dp.callback_query_handler(lambda c: c.data == 'kwiz')
async def process_callback_kwiz(callback_query: types.CallbackQuery):
    user = db.get_user_info(callback_query.from_user.id)
    logging.info(f'Информация по юзеру в КВИЗ: {user}')
    await bot.send_message(callback_query.from_user.id, 'Играм в КВИЗ')


@dp.message_handler(commands=['start'])
async def start_fnc(message: types.Message):
    # получаем информацию о пользователе
    user = db.get_user_info(message.from_user.id)

    #если пользователя не существует в БД, то добавим его
    if not(user):
        db.add_user_info(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
        user = db.get_user_info(message.from_user.id)

    logging.info(f'Информация по юзеру в команде start: {user}')
    logging.info(f'Получено сообщение от {message}')
    await message.answer(f'Привет, во что будем играть?', reply_markup = inline_games)
    logging.info(f'user id из JSON {type(message.from_user.id)}')
    logging.info(f'user id из ADMIN_ID {type(ADMIN_ID)}')
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
