import re

import asyncio
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from games import what_where_when as www
from keyboards.inline import play_game, start_game, countTeamsKeyMark, hostInfo, shareMethodMrp, shareLinkMrp
from keyboards.inline.what_where_when import connInGame

from loader import dp, bot, db
from states.what_where_when import WhatWhereWhen as www_state
import logging

import qrcode

"""
#Пример state
 {
      "host_id": 3214253256,
      "is_host_player": 1,
      "teams": [
          {"host_id": 45235452,"team_name":"Зеленые"},
          {"host_id": 47679945,"team_name":"Красные"}
        ]
 }



"""


@dp.callback_query_handler(text="www")
async def settings_www_game_fnc(call: CallbackQuery, state: FSMContext):

    logging.info("зашли в settings_www_game_fnc")


    await call.message.answer("Укажите количество команд",reply_markup=countTeamsKeyMark)
    await www_state.getCountTeams.set()  # устанавливаем состояние, при котором мы ждем от пользователя количество команд
    #удалим сообщение со списком ИГР т.к. начали Что где когда
    await bot.delete_message(call.message.chat.id, call.message.message_id)




#начало игры
@dp.callback_query_handler(text="start_game", state=[www_state.readyPlay, www_state.inviteTeam])
async def start_www_game_fnc(call: CallbackQuery, state: FSMContext):

    cur_id = call.from_user.id
    state = await state.get_data()
    host_id = state.get("game_host")

    #если начать игру нажал хост, то запускаем стор с его ИД
    if not host_id:
        host_id = cur_id

    #проставляем в сторе готовоность к началу игру, по тому кто нажал кнопку
    async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:

        for team in data["teams"]:
            # ищем в командах команду нашего игрока
            if team["host_id"] == cur_id:
                team["readyPlay"] = 1

                #очистим предыдущие ответы
                db.set_answer(cur_id, 'Null')
                logging.info(" Перед заходом в старт игры team[readyPlay]" + str(team["readyPlay"]))
                break

    logging.info(" Перед заходом в старт игры call.message.message_id" + str(call.message.message_id))

    #старт игры
    asyncio.ensure_future(www.show_question_fnc(call.from_user.id, call.message.message_id))

    #await state.reset_state(with_data=False)
    await www_state.answerPlayer.set()
    #await www.run_game_fnc(host_id=call.from_user.id)
    #await www_game.run_game(call.from_user.id) #запускаем игру Что Где Когда



#начало игры для приглашенных
@dp.callback_query_handler(text="start_game", state=www_state.joinGame)
async def start_www_game_fnc(call: CallbackQuery, state: FSMContext):

    logging.info("Зашли в запуск старта игры для приглашенного")

    data = await state.get_data()
    logging.info("/joinGame state присоединения к игре: " + str(data))
    host_id = data["game_host"]

    async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:

        for team in data["teams"]:
            # ищем в командах команду нашего игрока
            if team["host_id"] == host_id:
                team["readyPlay"] = 1

    #переводим хоста в режим готовности к началу игры
    await www_state.answerPlayer.set()
    #await state.reset_state(with_data=False)
    #await www.run_game_fnc(chat_id=call.from_user.id)
    #await www_game.run_game(call.from_user.id) #запускаем игру Что Где Когда





@dp.callback_query_handler(state=www_state.getCountTeams)
async def set_teams_count_fnc(call: CallbackQuery, state: FSMContext):

    logging.info("зашли в set_teams_count_fnc")
    team_count = int(call.data)


    # вариант получения state другоим пользователей
    # state = dp.current_state(chat=message.chat.id, user=message.from_user.id

    # await state.update_data(countTeams = answer)
    # state = dp.current_state(chat=message.chat.id, user=message.from_user.id)

    # если цифра пропускаем дальше, если нет, то просим ввести цифру

    async with state.proxy() as data:
        data["host_id"] = call.from_user.id
        data["is_host_player"] = 0 #по умолчанию считаем что тот кто создал игру будет вести игру, а не играть
        data["conn_status_msg_id"] = None #здесь сохраняем id сообщения, в котором будем отображать статус подключений к игре
        data["cur_question"] = 0 #здесь сохраняем номер текущего вопроса


        data["teams"] = []

        # сколько команд, на столько и расширим словарь
        for i in range(team_count):
            data["teams"].append({"host_id": None, "name": None, "readyPlay": 0, "score": 0, "cur_answer": None})

        logging.info("Команды в хранилище, после указания команд " + str( data["teams"]))
    #переводим пользователя в state заполнения доп инфо о хосте игры
    await www_state.getHostInfo.set()
    await call.message.edit_text(f"Количество команд: {team_count}")
    await call.message.answer(f"Какая ваша роль?", reply_markup=hostInfo)




#узнаем будет ли пользователь играь
@dp.callback_query_handler(state=www_state.getHostInfo)
async def set_host_info_fnc(call: CallbackQuery, state: FSMContext):

    logging.info("зашли в set_host_info_fnc (узнаем будем ли хост ведущим или игроком)")

    is_host_player = int(call.data)
    host_role = "ведущий"
    text = "Укажите название команды 1"
    #по умолчанию значение 0, если передали 1, то обновим это значение
    if is_host_player == 1:
        text = "Укажите название команды, в которой будете играть вы"
        host_role = "игрок"
        await state.update_data(is_host_player=is_host_player)
    state = await state.get_state()
    logging.info("Команды в хранилище, после указания выбора роли хоста " + str(state))

    #переводим пользователя в state заполнения названия команд
    await www_state.getNameTeam.set()
    await call.message.edit_text(f"Ваша роль: {host_role}")
    await call.message.answer(text)




#в этом хендлере ждем названия команд
@dp.message_handler(state=www_state.getNameTeam)
async def get_name_teams_fnc(message:types.Message, state: FSMContext):

    logging.info("зашли в get_name_teams_fnc (заполняем наименования команд)")
    team_name = message.text
    show_teams = ""

    async with state.proxy() as data:


        is_host_player = data["is_host_player"]
        logging.info(f"is_host_player: {is_host_player}")

        #нужно ли хосту выбрать команду?
        is_host_need_choose_team = False

        #если хост будет игроком, то узнаем присвоели ли ему уже команда
        if data["is_host_player"] == 1:
            cnt_host_teams = sum(i['host_id'] == data["host_id"] for i in data["teams"]) #кол-во уже назначеннвх хосту команд

            #если нет ни одной команды где хост был бы хостом команды, то присвоим ему первую команду
            if cnt_host_teams == 0:
                is_host_need_choose_team = True

        for team in data["teams"]:


            #если есть незаполненные названия команд, то заполним их поступившим значением
            if team["name"] is None:
                team["name"] = team_name.title()

                #если хост будет игроком и ему еще не присвоена команда
                if is_host_need_choose_team:

                    team["host_id"] = message.from_user.id

                break


        cnt_noname_teams = sum(i['name'] is None for i in data["teams"]) #кол-во команд, которые еще не названы
        cnt_name_teams = sum(i['name'] is not None for i in data["teams"]) #кол-во уже названных команд



    #если есть команды без названия, то запросим указать их
    if cnt_noname_teams > 0:
        await message.answer(f"Укажите название команды {str(cnt_name_teams+1)}")
        return

    #вариант получения state
    #admin_state = await (dp.current_state(chat=402584072, user=402584072)).get_data()
    #state = dp.current_state(chat=message.chat.id, user=message.from_user.id
    #data = await state.get_data()

    #await state.reset_state(with_data=False)
    #await www_state.next()

    #если хост игры будет играть, то он должен сразу выбрать команду
    #if is_host_player == 1:

    await message.answer("Игра успешно создана! 🦉", reply_markup=connInGame)
    await www_state.inviteTeam.set()

# узнаем каким способом пользователь будет приглашать людей в игру
@dp.callback_query_handler(state=www_state.inviteTeam)
async def invite_teams_fnc(call: CallbackQuery, state: FSMContext):
    #если хост играет сам с собой то пропускаем момент приглашения в игру
    #if cnt_name_teams == 1 and is_host_player == 1:

    #    await message.answer("Готовы?", reply_markup=start_game)

        # переводим в state ожидания других игроков


    #else:
    #переводим хоста в решим ожидания подключения других игроков
    bot_username = (await bot.get_me()).username
    id_referal = call.from_user.id

    bot_link = f"https://t.me/{bot_username}?start={id_referal}"
    # имя конечного файла
    filename = f"media/pics/inviteQRCODE{id_referal}.png"
    # генерируем qr-код
    img = qrcode.make(bot_link)
    # сохраняем img в файл
    img.save(filename)

    state = await state.get_data()
    # если хост не играет или команд больше одной , то отправляем QRCODE
    if state["is_host_player"] == 0 or len(state["teams"]) > 1:
        await bot.send_photo(call.message.chat.id, photo=open(filename, 'rb'))

    asyncio.ensure_future(www.wait_teams_fnc(call.from_user.id, call.message.message_id))


    #await message.answer(show_teams, reply_markup=shareMethodMrp)

    # переводим хоста в решим ожидания подключения других игроков
    # state.reset_state(with_data=False)
    # await message.answer(show_teams, reply_markup=start_game)


#реализация кнопки Пригласить в игру
@dp.inline_handler(state=www_state.inviteTeam)
async def inline_handler(query: types.InlineQuery):
    logging.info("зашли в inline_handler (для вывода кнопки Приласить друга)")

    """
    user_links = [["KEY", "LINK"]]
    if len(user_links) == 0:
        switch_text = "У вас нет сохранённых ссылок. Добавить »»" \
            if len(query.query) == 0 \
            else "Не найдено ссылок по данному запросу. Добавить »»"
        return await query.answer(
            [], cache_time=60, is_personal=True,
            switch_pm_parameter="add", switch_pm_text=switch_text)
    """

    bot_username = (await bot.get_me()).username
    id_referal = query.from_user.id

    bot_link = f"https://t.me/{bot_username}?start={id_referal}"


    article = types.InlineQueryResultArticle(
        id="1",
        title="Пригласить в игру",
        description=f"",
        url="https://t.me/party_hard_bot",
        hide_url=False,
        thumb_url=f"https://i.ytimg.com/vi/EMNKInfWanE/maxresdefault.jpg",
        input_message_content=types.InputTextMessageContent(
            message_text=f"Вас оиждают в игре <b>Что? Где? Когда?</b> перейдите по ссылке {bot_link}!",
            parse_mode="HTML"
        ))


    await query.answer([article], cache_time=60, is_personal=True)






#в этом хендлере ждем подключения к игре игроков
@dp.callback_query_handler(state=www_state.joinGame)
async def join_game_fnc(call: CallbackQuery, state: FSMContext):

    logging.info("зашли в join_game_fnc ")


    team_name = call.data
    data = await state.get_data()
    logging.info("/joinGame state присоединения к игре: " + str(data))
    host_id = data["game_host"]

    async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:

        for team in data["teams"]:
            #как тольок нашли имя которое указал пользователь, назначаем этого пользователя хостом этой команды
            if team["name"] == team_name:
                team["host_id"] = call.from_user.id

    #переводим игрока в ожидание команд
    await www_state.readyPlay.set()
    asyncio.ensure_future(www.wait_teams_fnc(chat_id=call.message.chat.id, mess_id=call.message.message_id))

    #await call.message.answer("Вы успешно подключились к игре! Ожидайте, игра скоро начнется")
    #await call.message.edit_text(text= f"Ваша команда: <b>{team_name}</b>")

    #отправим уведомление хосту о том, что пользователь подключился к игре
    await bot.send_message(chat_id=host_id, text=f"{call.from_user.full_name} ({call.from_user.username}) успешно подключился(-ась) к игре")


