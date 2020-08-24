import config
import logging
import time

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
#задаем уроверь логов
logging.basicConfig(level=logging.INFO)

#инициируем бота 
bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

#соединяемся с БД
db = SQLighter('taran_as_official_bot.db')

#список возможных возможностей бота
markup_games = types.InlineKeyboardMarkup(row_width=1)
btn_chgk_game = types.InlineKeyboardButton("Что, где, когда?", callback_data='chgk')
#btn_new_game = types.InlineKeyboardButton("Новая игра", callback_data='new')
markup_games.add(btn_chgk_game)

#кнопки для игры Что Где Когда?
markup_give_min = types.InlineKeyboardMarkup(row_width=1)
btn_give_min = types.InlineKeyboardButton("Дать минуту", callback_data='timer_minute')
markup_give_min.add(btn_give_min)

markup_skip = types.InlineKeyboardMarkup(row_width=1)
btn_skip_time = types.InlineKeyboardButton("Досрочный ответ", callback_data='show_answer')
markup_skip.add(btn_skip_time)

markup_next_quest = types.InlineKeyboardMarkup(row_width=2)
btn_next_question = types.InlineKeyboardButton("Далее", callback_data='next_question')
btn_finish_game = types.InlineKeyboardButton("Выход", callback_data='exit')
markup_next_quest.add(btn_next_question, btn_finish_game)


markup_team_count = types.InlineKeyboardMarkup(row_width=4)
btn_1 = types.InlineKeyboardButton("1", callback_data='setup_team')
btn_2 = types.InlineKeyboardButton("2", callback_data='setup_team')
btn_3 = types.InlineKeyboardButton("3", callback_data='setup_team')
btn_4 = types.InlineKeyboardButton("4", callback_data='setup_team')

markup_team_count.add(btn_1, btn_2, btn_3, btn_4)

#извлекаем вопросы из БД
quest = db.get_questions()
quest_num = 0

#переменная для остановки таймера в минуту
stop_timer = False



#функция для увеличения счетчика массива
def next_q_num():
    global quest_num 
    quest_num = quest_num + 1

def init_chgk():
    global quest_num, stop_timer
    quest_num = 0
    stop_timer = False


#Отправка следующего вопроса
async def get_next_quest(message: types.Message):
    #если вопросы закончились, то завершаем игру
    #print(str(quest_num) + ' - ' + str(len(quest)))
    if(quest_num == len(quest)):
        await bot.send_message(chat_id = message.chat.id, text = 'Извините, но вопросы закончились😔\nМожете выбрать другую игру', reply_markup = markup_games)
    else:
        await bot.send_message(chat_id = message.chat.id, text = quest[quest_num][2])
        await bot.send_message(chat_id = message.chat.id, text='⌛',reply_markup=markup_give_min)



async def get_answer(message: types.Message):
    await bot.send_message(chat_id = message.chat.id, text='Ответ: ' + quest[quest_num][3] + '\nКомментарий: ' + quest[quest_num][4])
    await bot.send_message(chat_id = message.chat.id, text=str(quest_num+1) + ' из ' + str(len(quest)) + ' пройден ✅',reply_markup=markup_next_quest)

    #Переходим к следующему вопросу
    next_q_num()
 

@dp.callback_query_handler(text = 'chgk')
async def process_callback_chgk(call: types.CallbackQuery):
    db.add_log(call.message.from_user.id, 1)
    #задем переменные
    init_chgk()
    await bot.send_message(call.from_user.id, 'Хорошо, вот первый вопрос!😈')
    await get_next_quest(call.message)



@dp.callback_query_handler(text = 'timer_minute')
async def process_callback_give_minute(call: types.CallbackQuery):
    #даем минуту
    #await post_minute(call.message)

    for i in range(1,60):

        if(not stop_timer):
            time.sleep(1)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(60 - i), reply_markup = markup_skip)
        else:
            return
    
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Время вышло!')
    time.sleep(1)
    await get_answer(call.message)
    
    

@dp.callback_query_handler(text = 'show_answer')
async def process_callback_show_answer(call: types.CallbackQuery):
    #завершаем работу таймера
    global stop_timer
    stop_timer = True

    #убираем кнопку, котроую нажали
    await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=None)

    #выводим ответ
    await get_answer(call.message)

    #возвращаем работу таймера
    stop_timer = False

@dp.callback_query_handler(text = 'next_question')
async def process_callback_next_question(call: types.CallbackQuery):
    #убираем предыдущую кнопку
    await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=None)
    await get_next_quest(call.message)

#выход из игры
@dp.callback_query_handler(text = 'exit')
async def process_callback_exit(call: types.CallbackQuery):
    await bot.send_message(chat_id = call.message.chat.id, text = 'Во что будем играть?😊', reply_markup = markup_games)


#команда старт
@dp.message_handler(commands=['start'])
async def wellcome(message: types.Message):

    #для начала добавим пользователя в лог
    if(not db.subscriber_exists(message.from_user.id)):
        #если нет его, то добавим
        db.add_subscriber(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
        db.close()

    sti = open('image/cat.png','rb')
    await bot.send_sticker(message.chat.id, sti)
    time.sleep(1)
    
    #await message.send_message("Привет!", reply_markup=markup_inline)
    await bot.send_message(message.chat.id, "Привет, {0.first_name}! Во что будем играть?".format(message.from_user),parse_mode='html',reply_markup=markup_games)

 


#Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    #проверяем наличие пользователя в БД
    if(not db.subscriber_exists(message.from_user.id)):
        #если нет его, то добавим
        db.add_subscriber(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    else:
        db.update_subscription(message.from_user.id, 1)

    await message.answer("Вы успешно подписались на рассылку!")


#отписка
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    #проверяем наличие пользователя в БД
    if(not db.subscriber_exists(message.from_user.id)):
        #если нет его, то добавим
        db.add_subscriber(message.from_user.id, 2)
        await message.answer("Ранее вы не были подписаны")
    else:
        db.update_subscription(message.from_user.id, 2)
        await message.answer("Вы успешно отписаны от меня")



#запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True, timeout = 70)