import logging
import psycopg2
import re
from data import config
#from data import debug_config as config
from aiogram import types

class PostgreSQL:

    #logging.basicConfig(level=logging.INFO)

    def __init__(self):
        logging.info("Создался экземпляр БД")

        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = psycopg2.connect(
                            database=config.DATABASE,
                            user=config.DBUSER,
                            password=config.DBPASS,
                            host=config.DBHOST,
                            port=config.DBPORT
                )
        except Exception as e:
            logging.info('Ошибка при подключении в БД: '+ str(e))
        finally:
            logging.info('Успешное подклчюение к БД')



    def run_query(self, query):
        """Execute SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                logging.info("Выполнение запроса: " + query)
                cur.execute(query) #выпоняем запрос

                logging.info('cur.rowcount:' + str(cur.rowcount))

                result = None

                #если при выполнении запрос вернулась
                if re.search(r'SELECT', cur.statusmessage) :
                    result = cur.fetchone()

                self.conn.commit()
                cur.close()
                return result
        except Exception as e:
            logging.info('Ошибка при выполнении запроса ' + query + '\n' + str(e))
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                logging.info('Успешное отключение от БД')




    def get_questions(self, app_id=1):#1 - Что? Где? Когда?
        #Вытягиваем все вопросы к игре, что где когда
        sql_query = "select * from questions_tbl where id_application = {0}".format(app_id)
        return self.run_query(sql_query)



    def get_subscriptions(self, status = 1):#1 - Подписан, 2 - Не подписан
        #Получаем всех активных пользователей
        sql_query = "select * from subscribe_users where id_status = " + str(status)
        return self.run_query(sql_query)

    def subscriber_exists(self, user_id):
        #Проверяем есть ли уже юзер в базе
        sql_query = "select * from users_tbl where id_user = " + str(user_id)

        #если длина результат больше одного символа то считаем что подписчик существует
        return bool(len(self.run_query(sql_query)))

    def get_user_info(self, msg: types.Message):
        #Вытягиваем всю необходимую инфу о пользователе
        sql_query = "select * from telegram_users_tbl where id = {0}".format(msg.from_user.id)

        result = self.run_query(sql_query)

        logging.info("Инфо о пользователе: " + str(result))
        logging.info("Инфо о пользователе из types : " + str(msg))

        return result


    def add_user_info(self, user_id, f_name = None, l_name = None, u_name = None, phone = 'Null'):
        #Добавляем нового подписчика или обновляем информацию
        sql_query = """insert into telegram_users_tbl as t (id, first_name,last_name,user_name,phone) 
                       values ({0},'{1}','{2}','{3}', {4})  
                        on conflict(id) do update
                        set first_name = coalesce('{1}', t.first_name),
                            last_name  = coalesce('{2}', t.last_name),
                            user_name  = coalesce('{3}', t.user_name),
                            phone      = coalesce( {4}, t.phone) ;""".format(user_id,f_name,l_name,u_name,phone)
        self.run_query(sql_query)

    def set_answer(self, user_id, answer):
        #Добавляем нового подписчика или обновляем информацию
        sql_query = """  INSERT INTO user_answers_tbl (id_user, answer)
                         VALUES ({0}, '{1}')
                         ON CONFLICT (id_user) DO UPDATE SET answer = EXCLUDED.answer;""".format(user_id,answer)
        self.run_query(sql_query)


    def get_answer(self, user_id):

        sql_query = "select * from user_answers_tbl where id_user = {0}".format(user_id)

        result = self.run_query(sql_query)

        logging.info("Инфо об ответах: " + str(result))

        return result

    def close(self):
        #Закрываем соединение с БД
        self.connection.close()