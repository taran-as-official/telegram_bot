
from debug_settings import (BOT_TOKEN) #при тесте это раскомментировать
#from bot.settings import (BOT_TOKEN) #при проде это раскомментировать
from aiogram import Bot, types
from asyncio import sleep
#import time
import logging

#Игра Что? Где? Когда?
class whatWhereWhen:

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        #self.quests = db.get_questions(1) # в базе данный, в таблице application игре Что?Где?Когда? соответствует id = 1
        self.quests = ['Первый', 'Второй']
        self.answers = ['Первый ответ', 'Второй ответ']
        self.quest_num = None
        self.quest_text = ""
        self.quest_answer = ""
        self.quest_comment = ""

        self.game_is_runnig = False
        self.stop_timer = False
        logging.info("QUESTIION: " + str(self.quests))


        self.markup_next_quest = types.InlineKeyboardMarkup(row_width=2)
        btn_next_question = types.InlineKeyboardButton("Далее", callback_data='www_next_question')
        btn_finish_game = types.InlineKeyboardButton("Выход", callback_data='www_exit')
        self.markup_next_quest.add(btn_next_question, btn_finish_game)

        self.markup_exit = types.InlineKeyboardMarkup(row_width=1)
        self.markup_exit.add(btn_finish_game)


        self.markup_early_answer = types.InlineKeyboardMarkup(row_width=1)
        btn_skip_time = types.InlineKeyboardButton("Досрочный ответ", callback_data='www_early_answer')
        self.markup_early_answer.add(btn_skip_time)


        self.markup_give_minute = types.InlineKeyboardMarkup(row_width=1)
        btn_give_min = types.InlineKeyboardButton("Дать минуту", callback_data='www_give_minute')
        btn_skip_time = types.InlineKeyboardButton("Досрочный ответ", callback_data='www_early_answer')

        self.markup_give_minute.add(btn_give_min)



    async def run_game(self, chat_id):
        self.game_is_runnig = True
        self.quest_num = 0
        self.stop_timer = False
        self.quest_text = "Хорошо, вот первый вопрос!😈\n\n" + self.quests[self.quest_num]
        #self.quest_answer = self.quests[self.quest_num]["answer"]
        #self.quest_comment = self.quests[self.quest_num]["comment"]

        await self.bot.send_message(chat_id = chat_id, text = self.quest_text)
        await self.bot.send_message(chat_id = chat_id, text ='⌛',reply_markup=self.markup_give_minute)


    async def show_answer(self, chat_id):
        await self.bot.send_message(chat_id = chat_id, text='Ответ: ' + self.answers[self.quest_num] + '\nКомментарий: ' )

        if self.quest_num+1 == len(self.quests):
            await self.bot.send_message(chat_id=chat_id, text='Спасибо за игру, вопросы закончились',
                                        reply_markup=self.markup_exit)
        else:
            await self.bot.send_message(chat_id = chat_id, text=str(self.quest_num+1) + ' из ' + str(len(self.quests)) + ' пройден ✅',reply_markup=self.markup_next_quest)



    async def early_answer(self):
        logging.info("Попали в early_answer: " + str(self.stop_timer))
        self.stop_timer = True
        logging.info("Прошли в early_answer: " + str(self.stop_timer))

    async def give_minute(self, chat_id, message_id):
        logging.info("Зашли в give_minute: " + str(self.stop_timer))
        text = 'Время вышло'
        if not self.stop_timer:
            logging.info("Зашли в give_minute перед циклом: " + str(self.stop_timer))

            for i in range(1, 60):
                logging.info("Зашли в give_minute в цикле " + str(i) + ": " + str(self.stop_timer))

                if self.stop_timer:
                    logging.info("Зашли в give_minute в досрочный ответ " + str(i) + ": " + str(self.stop_timer))

                    self.stop_timer = False
                    text = 'Досрочный ответ'
                    break
                await sleep(1)
                logging.info("Зашли в give_minute в цикл " + str(i) + " завершен: " + str(self.stop_timer))
                await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=str(60 - i), reply_markup=self.markup_early_answer)
                #await self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,reply_markup=self.markup_early_answer)





        else:
            self.stop_timer = False
            text = 'Досрочный ответ'

        await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
        await self.show_answer(chat_id)
        return


    async def next_question(self, chat_id):

        self.quest_num += 1


        self.quest_text = self.quests[self.quest_num]
        #self.quest_answer = self.quests[self.quest_num][3]
        #self.quest_comment = self.quests[self.quest_num][4]
        await self.bot.send_message(chat_id = chat_id, text = self.quest_text)
        await self.bot.send_message(chat_id = chat_id, text ='⌛',reply_markup=self.markup_give_minute)

