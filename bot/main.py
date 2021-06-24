from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
from postgres import PostgreSQL
from debug_settings import (BOT_TOKEN, ADMIN_ID, BOT_ID)
from games import whatWhereWhen as www

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.DEBUG)


#dp.middleware.setup(LoggingMiddleware())
db = PostgreSQL()




www_game = www()



#инициализируем конпки
www_game_btn = types.InlineKeyboardButton('Что? Где? Когда?', callback_data='www_game')
kwiz = types.InlineKeyboardButton('Квиз', callback_data='kwiz')
inline_games = types.InlineKeyboardMarkup().add(www_game_btn,kwiz)


@dp.callback_query_handler(lambda c: c.data == 'www_game')
async def process_callback_www_game(callback_query: types.CallbackQuery):

    await www_game.run_game(callback_query.from_user.id)

@dp.callback_query_handler(lambda c: c.data == 'www_give_minute')
async def process_callback_www_give_minute(callback_query: types.CallbackQuery):

    await www_game.give_minute(callback_query.from_user.id,callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'www_early_answer')
async def process_callback_www_give_minute(callback_query: types.CallbackQuery):

    await www_game.early_answer()

@dp.callback_query_handler(lambda c: c.data == 'www_next_question')
async def process_callback_www_next_question(callback_query: types.CallbackQuery):

    await www_game.next_question(callback_query.from_user.id)

@dp.callback_query_handler(lambda c: c.data == 'www_exit')
async def process_callback_www_exit(callback_query: types.CallbackQuery):

    await start_fnc(callback_query.message)

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

    if message.from_user.id not in [ADMIN_ID, BOT_ID] :
        await bot.send_message(ADMIN_ID, f'{message.from_user.full_name} присоединился к боту')


@dp.message_handler()
async def echo(message: types.Message):

	logging.warning(str(message))
	await bot.send_message(message.chat.id, message.text)



if __name__ == '__main__':
    executor.start_polling(dp)