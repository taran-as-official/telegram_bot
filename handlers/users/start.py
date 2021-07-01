from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from states.what_where_when import WhatWhereWhen as www_state

from keyboards.inline import choose_game
from loader import dp, bot
import logging


@dp.message_handler(CommandStart(), state="*")
async def bot_start_fnc(message: types.Message, state: FSMContext):
    logging.info("зашли в bot_start_fnc")

    #await state.reset_state()

    is_refereal = message.get_args()
    #cur_state = await state.get_data()
    #logging.info("/start is_refereal текущего пользователя: " + str(is_refereal))

    #logging.info("/start state текущего пользователя: " + str(cur_state))

    if is_refereal:
        #добавим в state присоединившегося пользователя хоста игры
        await state.update_data(game_host=is_refereal)

        #Выведем из state хоста список команд и предложим выбрать присоединившемуся пользователю
        async with (dp.current_state(chat=is_refereal, user=is_refereal)).proxy() as data:
            logging.info("/start state хоста игры host_state: " + str(data))

            for team in data["teams"]:
                team = InlineKeyboardButton(f'{team["name"]}', callback_data=team["name"])
                choose_team = InlineKeyboardMarkup().add(team)

        await www_state.joinGame.set()
        await message.answer("Выберите команду", reply_markup=choose_team)
        return
        #host_state = await (dp.current_state(chat=is_refereal, user=is_refereal)).get_data()

    await state.reset_state()
    await message.answer(f"Привет, {message.from_user.full_name}! В какую игру будем играть?",reply_markup = choose_game)

