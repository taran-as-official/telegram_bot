
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from loader import dp

from games import what_where_when as www #расскоментить при зтестировании
import asyncio
from keyboards.inline import choose_game, play_game
import logging
from states.what_where_when import WhatWhereWhen as www_state




@dp.callback_query_handler(text="start_timer")
async def start_minute_fnc(call: CallbackQuery):
    logging.info("Зашли в start_time")
    asyncio.ensure_future(www.start_minute_fnc(call.from_user.id, call.message.message_id))
    #await www.start_minute_fnc(call.from_user.id, call.message.message_id)
    logging.info("Установили таймер")


@dp.callback_query_handler(text="stop_timer")
async def stop_minute_fnc(call: CallbackQuery):

    await www.stop_timer_fnc()



    #await www.next_question_fnc(call.from_user.id)

@dp.callback_query_handler(text="exit", state=www_state.answerPlayer)
async def exit_from_game_fnc(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup() #удаляем кнопку выход
    await state.reset_state()
    await call.message.answer(f"В какую игру будем играть теперь?", reply_markup=choose_game)

#в этом хендлере отлавливаем пожелания пользователей продолжить игру
@dp.callback_query_handler(text="next_question", state=www_state.answerPlayer)
async def next_question_fnc(call: CallbackQuery):

    state = await dp.get_current().current_state().get_data()
    # пытаемся найти у игрока ключ с полем хоста
    host_id = state.get("game_host")

    # если такой ключ не найден, значит функцию запустил хост и смотрим в его state
    if not host_id:
        host_id = call.from_user.id

    i = 1
    # теперь переводим игру в другой цикл, где будем показывать готовность игроков к началу игры

    #Т.к. пользователь нажал кнопку, проставим ему флаг готовности
    async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:

        # обновим статус по каждой команде
        for team in data["teams"]:
            if team["host_id"] == call.from_user.id:
                team["readyPlay"] = 1


    asyncio.ensure_future(www.show_question_fnc(call.from_user.id, call.message.message_id))


#в этом хендлере отлавливаем ответы пользователей
@dp.message_handler(state=www_state.answerPlayer)
async def get_answer_fnc(mess: Message):

    answer = str(mess.text).lower()

    await www.set_answer_fnc(mess.from_user.id, answer)





#в этом хендлере отлавливаем нестандартное поведение
@dp.message_handler(state="*")
async def debug_message_handler_fnc(call: CallbackQuery):
    await call.message.answer("Вы попали в Default Колбак Хендлер")
