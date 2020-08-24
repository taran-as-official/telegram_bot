import sqlite3
from datetime import datetime

class SQLighter:
    def __init__(self, database_file):
        #Подключаемся к БД и сохраняем курсор соединения
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_questions(self, app_id=1):#1 - Что? Где? Когда?
        #Получаем всех активных пользователей
        with self.connection:
            return self.cursor.execute("select * from `questions_tbl` where `id_application` = ?", (app_id,)).fetchall()



    def get_subscriptions(self, status = 1):#1 - Подписан, 2 - Не подписан
        #Получаем всех активных пользователей
        with self.connection:
            return self.cursor.execute("select * from `subscribe_users` where `id_status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        #Проверяем есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute("select * from `users` where `id_user` = ?", (user_id,)).fetchall()
            return bool(len(result))


    def add_subscriber(self, user_id, f_name, l_name, u_name, status = 0):
        c_date = datetime.now()
        #Добавляем нового подписчика
        with self.connection:
            self.cursor.execute("insert into `users`(`id_user`,`first_name`,`last_name`,`user_name`,`create_date`) values (?, ?, ?, ?, ?)", (user_id, f_name, l_name, u_name, c_date))
            return self.cursor.execute("insert into `subscribe_users`(`id_user`,`id_status`,`create_date`) values (?, ?, ?)", (user_id, status, c_date))

    def update_subscription(self, user_id, status):
        #Обновляем статус подписки
        l_date = datetime.now()
        return self.cursor.execute("update `subscribe_users` set `id_status` = ?, `last_date` = ? where `id_user` = ?", (status, user_id, l_date))

    
    def add_log(self, user_id, id_application):
        
        with self.connection:
            #Проверяем есть ли уже запись в логе с этим пользователем
            log_exists = self.cursor.execute("select id_log, id_user, run_count from `application_log_tbl` where `id_user` = ? and `id_application` = ?", (user_id, id_application)).fetchall()
            if(log_exists == []):
                return self.cursor.execute("insert into `application_log_tbl`(`id_application`,`id_user`,`create_date`) values (?, ?, ?)", (id_application, user_id, datetime.now()))
            else:
                #получаем количесто запусков игры из существующего лога
                run_count = log_exists[0][2]
                #увеличиваем на 1
                run_count += 1
                #лог id берем из существующего лога
                log_id = log_exists[0][0]

                return self.cursor.execute("update `application_log_tbl` set `run_count` = ?, `lastdate` = ? where `id_log` = ? ", (run_count, datetime.now(), log_id))



    def close(self):
        #Закрываем соединение с БД
        self.connection.close()