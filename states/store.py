from loader import dp
import logging

class Game:

    #logging.basicConfig(level=logging.INFO)

    def __init__(self, user_id, team_count):
        logging.info("Создалась игра")

        self.gameHost = user_id
        self.isHostPlayer = 0
        self.currentQuestNum = 0

        #инициируем state
        #dp.current_state(chat=user_id, user=user_id).update_data(self)


    async def set_store(self,user_id):
        async with (dp.current_state(chat=user_id, user=user_id)).proxy() as data:
            data["host_id"] = self.gameHost  # хост игры
            data["is_host_player"] = self.isHostPlayer  # по умолчанию считаем что тот кто создал игру будет вести игру, а не играть

    async def get_store(self,user_id):
        return dp.current_state(chat=user_id, user=user_id).get_data()

#async def create_game_fnc(chat_id, mess_id):
#async with (dp.current_state(chat=is_refereal, user=is_refereal)).proxy() as data:


"""
            data["host_id"] = user_id #хост игры
            data["is_host_player"] = self.isHostPlayer  # по умолчанию считаем что тот кто создал игру будет вести игру, а не играть
            data["cur_question"] = self.currentQuestNum  # здесь сохраняем номер текущего вопроса
            data["teams"] = [] #список команд

            # сколько команд, на столько и расширим словарь
            for i in range(team_count):
                data["teams"].append({"host_id": None, "name": None, "readyPlay": 0, "score": 0, "cur_answer": None})

"""