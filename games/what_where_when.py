import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import shareLinkMrp
from loader import bot, dp, db
from asyncio import sleep
import re
import logging

from keyboards.inline.what_where_when import give_minute, early_answer, next_question, exit_game, start_game

#Игра Что? Где? Когда?



quests = ['Швейцарец Жан-Жак Бабель подсчитал, что с 3500 года до н.э. человечество провело всего лишь 292 года без... Чего?',
          'Человек не чувствует запахов пока',
          'Суто, Юго-Восточная Африка: "Неизведанная даль беспокоит сердце, а знакомая окрестность — только ..." Что?',
          'У многих скоморохов в древности была погремушка из бычьего пузыря. А плоды какого растения находились внутри этого пузыря?',
          'В среднем человек проводит 6 месяцев своей жизни ожидая',
          'В одном американском городе местные библиотекари устроили необычную выставку. Среди разнообразных бумажек посетители могли увидеть ломтики сала, кухонные ножи, хирургические перчатки и лезвия для бритья. Чем в свое время служили экспонаты?',
          'Если есть слишком много моркови можно ... Что?',
          'На вершине Эвереста можно найти останки ... Кого/Чего?',
          'В последнее время на Западе на некоторых туристических картах, для удобства пеших прогулок, изолинии пеших равноудаленности от отеля и расстояния отмечаются не в метрах или км., а в чем?',
          'Собаки определяют, что их хозяин напуган, по запаху ... Чего?',
          'Скатерти изначально использовались еще и как ... Что?',
          'На стенах пирамиды Сахурн можно встретить изображения работающих людей, одетых в нечто, похожее на плавки с квадратным куском кожи на задней части. Какова профессия этих людей?'
          ]
answersPattern = ['войн'
                  ,'спит'
                  ,'ноги'
                  ,'горох'
                  ,'свет|зелен'
                  ,'закладк|вклад'
                  ,'желт'
                  ,'морск|рыб|водн|водя'
                  ,'час|минут|врем'
                  ,'пот'
                  ,'полотенц'
                  ,'греб'
                  ]
answers = ['без войн'
           ,'спит'
           ,'ноги'
           ,'горох'
           ,'заленый свет светофора'
           ,'закладки'
           ,'пожелтеть'
           ,'морских существ'
           ,'в часах ходьбы'
           ,'пота'
           ,'полотенца'
           ,'гребцы'
           ]
quest_comment = []
game_is_runnig = True
quest_number = 0
stop_timer = False


user_answers = []


score = 0

# вспомогательная функция, в которой мы будет отображать подключение
async def wait_teams_fnc(chat_id, mess_id):
    i = 1

    is_host = False
    # logging.info("Зашли в start_minute в цикле " + str(i) + ": " + str(early_answ))
    state = await dp.get_current().current_state().get_data()

    # пытаемся найти у игрока ключ с полем хоста
    host_id = state.get("game_host")

    # если такой ключ не найден, значит функцию запустил хост и смотрим в его state
    if not host_id:
        host_id = chat_id
        is_host = True

    while True:

        async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:
            show_teams = "Ожидание подключение других участников:\n\n"

            for team in data["teams"]:
                if not team["host_id"]:
                    status_text = "." * i + " "
                else:
                    status_text = "подключен ✅"

                # формируем итоговый вывод команд для пользователя
                show_teams = show_teams + "<b>" + str(team["name"]) + "</b> - " + status_text + "\n"
                cnt_noconn_teams = sum(i['host_id'] is None for i in data["teams"])  # кол-во команд, которые еще не подключились

        i += 1

        if i == 4:
            i = 1

        #как только закончились команды, которым не назначен хост, выходим из цикла
        if cnt_noconn_teams == 0:
            show_teams = re.sub(r"Ожидание подключение других участников:", f"Все участники успешно подключились:", show_teams)

            await bot.edit_message_text(chat_id=chat_id, message_id=mess_id, text=show_teams)
            break

        #если функция запущена для хоста игры, то выводим ему результат с кнопкой Поделиться
        if is_host:
            show_teams = show_teams + "\n\nДайте игрокам отсканировать QRCODE или пришлите им ссылку"
            await bot.edit_message_text(chat_id=chat_id, message_id=mess_id, text=show_teams, reply_markup=shareLinkMrp)
        else:
            await bot.edit_message_text(chat_id=chat_id, message_id=mess_id, text=show_teams)
        # await self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,reply_markup=self.markup_early_answer)


        await sleep(1)


    rules = "<b>Правила:</b>\n\n1. Вопросы не появятся, пока каждый игрок подтвердит готовность\n\n2. После нажатия кнопки \"Начать игру\"\\\"Далее\" у вас будет 60 секунд, чтобы написать свой ответ\n\n3. В зачет идет последний отправленный ответ"
    await bot.send_message(chat_id=chat_id, text="Теперь, как только все участники будут готовы, игра начнется!\n\n" + rules, reply_markup=start_game)



async def show_question_fnc(user_id, mess_id):

    state = await dp.get_current().current_state().get_data()
    # пытаемся найти у игрока ключ с полем хоста
    host_id = state.get("game_host")

    # если такой ключ не найден, значит функцию запустил хост и смотрим в его state
    if not host_id:
        host_id = user_id


    i=1
    # теперь переводим игру в другой цикл, где будем показывать готовность игроков к началу игры
    while True:

        # ogging.info("Зашли в start_minute в цикле " + str(i) + ": " + str(early_answ))
        async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:
            show_teams = "Ожидание готовности участников:\n\n"

            # обновим статус по каждой команде
            for team in data["teams"]:

                if team["readyPlay"] == 0:
                    status_text = "." * i
                else:
                    status_text = "готов ✅"

                # формируем итоговый вывод команд для пользователя
                show_teams = show_teams + "<b>" + str(team["name"]) + "</b> - " + status_text + "\n"

            for team in data["teams"]:
                if team["host_id"] == user_id:
                    await bot.edit_message_text(chat_id=user_id, message_id=mess_id, text=show_teams)
                    break

            cnt_noconn_teams = sum(
                i['readyPlay'] == 0 for i in data["teams"])  # кол-во команд, которые еще не готовы

        i += 1

        if i == 4:
            i = 1
        # await self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,reply_markup=self.markup_early_answer)

        await sleep(1)

        # как только закончились команды, которые не готовы - начинаем игру через 5 секунд
        if cnt_noconn_teams == 0:

            time_to_start = 3

            show_teams = re.sub(r"Ожидание готовности участников:",
                                f"Все готовы игра начнется через <b>{time_to_start}</b>", show_teams)

            for x in range(time_to_start):
                # меняем цифру каждую секунду
                show_teams = re.sub(r"\d", str(time_to_start - x), show_teams)
                # отобразим каждой команде статус других команд
                for team in data["teams"]:
                    if team["host_id"] == user_id:
                        await bot.edit_message_text(chat_id=team["host_id"], message_id=mess_id, text=show_teams)
                        break

                await sleep(1)
            break



    async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:
        global quest_number
        quest_number = data["cur_question"]



        time_to_answer = 60
        show_quest = f"Вопрос №{quest_number + 1}:\n\n<b>{quests[quest_number]}</b>\n\n⌛ <b>{time_to_answer}</b>"
        # даем 11 секунд на ознакомление с вопросом
        for x in range(time_to_answer):
            show_quest = re.sub(r"<b>\d+<\/b>", f"<b>{time_to_answer - x}</b>", show_quest)

            for team in data["teams"]:
                if team["host_id"] == user_id:
                    await bot.edit_message_text(chat_id=team["host_id"], message_id=mess_id, text=show_quest)
                    break

            await sleep(1)


        #быстро сбрасываем активность, чтобы в момент ответа пользователю не защитали ответ
        for team in data["teams"]:
            team["readyPlay"] = 0  # сбрасываем готовность, для ожидания других участников в новом вопросе
     


    #ПРОВЕРКА ОТВЕТОВ


    #обновим state
    #async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:
        logging.info("хранилищe " + str(data["teams"]))
        #проверим на правильность ответов и предложим пойти дальше
        for team in data["teams"]:

            add_text = "❌"

            cur_answer = db.get_answer(team["host_id"])
            #если ответ совпадает, то прибавим бал
            logging.info("хранилищe " + str(cur_answer))
            logging.info("Ответ в массиве " + str(answers[quest_number]).lower())


            #если пользователь хоть что то ответил, то зайдем проверять на корректность его ответ
            if cur_answer:
                #правильный ответ является шаблоном для регулярного выражения, чтобы максимально засчитывать верные ответы
                if re.search(answersPattern[quest_number], cur_answer[1]):
                    team["score"] += 1
                    add_text = "✅"


            show_quest = re.sub(r"(.+<b>\d+<\/b>)$", add_text, show_quest)
            # удалим инфу о таймере и оставим только текст вопроса
            if team["host_id"] == user_id:
                await bot.edit_message_text(chat_id=team["host_id"], message_id=mess_id, text=show_quest)

        #убираем верно или неверно,
        add_text = "Верно✅" if add_text == "✅" else "Неверно❌"


        if quest_number + 1 == len(quests):
            await bot.send_message(chat_id=user_id,
                                   text=add_text + '\n\nОтвет: ' + answers[quest_number] + "\n\n" + str(quest_number + 1) + ' из ' + str(len(quests)) + ' пройден ✅')

            result = "Итого:\n\n"

            #отсортируем список, будем выводить лидирующие команды первыми
            data["teams"].sort(key=lambda dictionary: dictionary['score'], reverse=True)

            for team in data["teams"]:
                result = result + team["name"] + ": <b>" + str(team["score"]) + "</b>\n"
            await bot.send_message(chat_id=user_id, text=result + '\n\nСпасибо за игру, вопросы закончились',
                                   reply_markup=exit_game)
        else:
            await bot.send_message(chat_id=user_id,
                                   text=add_text + '\n\nОтвет: ' + answers[quest_number] + "\n\n" + str(quest_number + 1) + ' из ' + str(len(quests)) + ' пройден ✅',
                                   reply_markup=next_question)

        #переходим к следующему вопросу
        data["cur_question"] += 1


async def run_game_fnc(user_id, mess_id):

    state = await dp.get_current().current_state().get_data()
    # пытаемся найти у игрока ключ с полем хоста
    host_id = state.get("game_host")

    # если такой ключ не найден, значит функцию запустил хост и смотрим в его state
    if not host_id:
        host_id = user_id


    await show_question_fnc(user_id, mess_id)





async def set_answer_fnc(user_id, message_text):

    logging.info(f"message_text: {message_text}")
    db.set_answer(user_id,message_text)
    await bot.send_message(user_id,"Ответ принят")


async def stop_timer_fnc():
    global stop_timer
    stop_timer = True


async def show_answer_fnc(user_id, mess_id):
    # ПРОВЕРКА ОТВЕТОВ
    state = await dp.get_current().current_state().get_data()
    # пытаемся найти у игрока ключ с полем хоста
    host_id = state.get("game_host")

    # если такой ключ не найден, значит функцию запустил хост и смотрим в его state
    if not host_id:
        host_id = user_id

    i = 1
    async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:

        # обновим state
        # async with (dp.current_state(chat=host_id, user=host_id)).proxy() as data:
        logging.info("хранилищe " + str(data["teams"]))
        # проверим на правильность ответов и предложим пойти дальше
        for team in data["teams"]:

            add_text = "Неверно!"

            if team["host_id"] == user_id:

                # если ответ совпадает, то прибавим бал
                logging.info("хранилищe " + str(data["teams"]))

                logging.info("ответ из хранилища " + str(team["cur_answer"]))
                logging.info("ответ из пакета " + str(user_answers))



                if team["cur_answer"] == str(answers[quest_number]).lower():
                    team["score"] += 1
                    add_text = "Верно!"


                show_quest = re.sub(r"Время на ответ <b>\d+<\/b>", add_text, show_quest)
                # удалим инфу о таймере и оставим только текст вопроса
                await bot.edit_message_text(chat_id=team["host_id"], message_id=mess_id, text=show_quest)

        if quest_number + 1 == len(quests):
            await bot.send_message(chat_id=user_id,
                                   text=add_text + '\n\nОтвет: ' + answers[quest_number] + '\nКомментарий: ' +
                                        quest_comment[quest_number] + "\n\n" + str(quest_number + 1) + ' из ' + str(
                                       len(quests)) + ' пройден ✅')
            await bot.send_message(chat_id=user_id, text='Спасибо за игру, вопросы закончились',
                                   reply_markup=exit_game)
        else:
            await bot.send_message(chat_id=user_id,
                                   text=add_text + '\n\nОтвет: ' + answers[quest_number] + '\nКомментарий: ' +
                                        quest_comment[quest_number] + "\n\n" + str(quest_number + 1) + ' из ' + str(
                                       len(quests)) + ' пройден ✅',
                                   reply_markup=next_question)

        # переходим к следующему вопросу
        data["cur_question"] += 1


"""""
async def stop_timer_fnc():
global stop_timer
stop_timer = True




async def start_minute_fnc(chat_id, message_id):
text = 'Время вышло'
global stop_timer
for i in range(1, 60):
#logging.info("Зашли в start_minute в цикле " + str(i) + ": " + str(early_answ))

if stop_timer:
 #logging.info("Зашли в start_minute в досрочный ответ " + str(i) + ": " + str(early_answ))

 stop_timer = False
 text = 'Досрочный ответ'
 break
await sleep(1)
#logging.info("Зашли в give_minute в цикл " + str(i) + " завершен: " + str(early_answ))
await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=str(60 - i), reply_markup=early_answer)
#await self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,reply_markup=self.markup_early_answer)



await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
await show_answer_fnc(chat_id)
return


async def next_question_fnc(chat_id):
global quest_num
quest_num += 1


quest_text = quests[quest_num]
#self.quest_answer = self.quests[self.quest_num][3]
#self.quest_comment = self.quests[self.quest_num][4]
await bot.send_message(chat_id = chat_id, text = quest_text)
await bot.send_message(chat_id = chat_id, text ='⌛',reply_markup=give_minute)

"""



"""""
async def run_game(self, chat_id):
    self.game_is_runnig = True
    self.quest_num = 0
    self.stop_timer = False
    self.quest_text = "Хорошо, вот первый вопрос!😈\n\n" + self.quests[self.quest_num]
    #self.quest_answer = self.quests[self.quest_num]["answer"]
    #self.quest_comment = self.quests[self.quest_num]["comment"]

    await bot.send_message(chat_id = chat_id, text = self.quest_text)
    await bot.send_message(chat_id = chat_id, text ='⌛',reply_markup=self.markup_give_minute)


async def show_answer(self, chat_id):
    await bot.send_message(chat_id = chat_id, text='Ответ: ' + self.answers[self.quest_num] + '\nКомментарий: ' )

    if self.quest_num+1 == len(self.quests):
        await bot.send_message(chat_id=chat_id, text='Спасибо за игру, вопросы закончились',
                                    reply_markup=self.markup_exit)
    else:
        await bot.send_message(chat_id = chat_id, text=str(self.quest_num+1) + ' из ' + str(len(self.quests)) + ' пройден ✅',reply_markup=self.markup_next_quest)



async def early_answer(self):
    logging.info("Попали в early_answer: " + str(self.stop_timer))
    self.stop_timer = True
    logging.info("Прошли в early_answer: " + str(self.stop_timer))


async def give_minute(self, chat_id, message_id):
    logging.info("Зашли в give_minute: " + str(self.stop_timer))
    text = 'Время вышло'

    for i in range(1, 60):
        logging.info("Зашли в give_minute в цикле " + str(i) + ": " + str(self.stop_timer))

        if self.stop_timer:
            logging.info("Зашли в give_minute в досрочный ответ " + str(i) + ": " + str(self.stop_timer))

            self.stop_timer = False
            text = 'Досрочный ответ'
            break
        await sleep(1)
        logging.info("Зашли в give_minute в цикл " + str(i) + " завершен: " + str(self.stop_timer))
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=str(60 - i), reply_markup=self.markup_early_answer)
        #await self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,reply_markup=self.markup_early_answer)



    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
    await show_answer(chat_id)
    return


async def next_question(self, chat_id):

    self.quest_num += 1


    self.quest_text = self.quests[self.quest_num]
    #self.quest_answer = self.quests[self.quest_num][3]
    #self.quest_comment = self.quests[self.quest_num][4]
    await bot.send_message(chat_id = chat_id, text = self.quest_text)
    await bot.send_message(chat_id = chat_id, text ='⌛',reply_markup=self.markup_give_minute)
"""