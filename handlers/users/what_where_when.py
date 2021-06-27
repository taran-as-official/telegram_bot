from aiogram.types import CallbackQuery

from loader import dp

from games import what_where_when as www #расскоментить при зтестировании
import asyncio
from keyboards.inline import choose_game

@dp.callback_query_handler(text_contains="www")
async def start_www_game_fnc(call: CallbackQuery):

    await www.run_game_fnc(chat_id=call.from_user.id)
    #await www_game.run_game(call.from_user.id) #запускаем игру Что Где Когда


@dp.callback_query_handler(text_contains="start_timer")
async def start_minute_fnc(call: CallbackQuery):

    asyncio.ensure_future(www.start_minute(call.from_user.id, call.message.message_id))
    #await www.start_minute_fnc(call.from_user.id, call.message.message_id)


@dp.callback_query_handler(text="stop_timer")
async def stop_minute_fnc(call: CallbackQuery):

    await www.stop_timer_fnc()


@dp.callback_query_handler(text="next_question")
async def next_question_fnc(call: CallbackQuery):

    await www.next_question_fnc(call.from_user.id)

@dp.callback_query_handler(text="exit")
async def exit_from_game_fnc(call: CallbackQuery):
    await call.message.edit_reply_markup() #удаляем кнопку выход
    await call.message.answer(f"В какую игру будем играть теперь?", reply_markup=choose_game)
