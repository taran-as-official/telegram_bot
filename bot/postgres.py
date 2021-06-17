import logging
import psycopg2
from bot.settings import (DATABASE, DBUSER, DBPASS, DBHOST, DBPORT)

class PostgreSQL:

    def __init__(self):
        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                con = psycopg2.connect(
                    database=DATABASE,
                    user=DBUSER,
                    password=DBPASS,
                    host=DBHOST,
                    port=DBPORT
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
                cur.execute(query)
                result = cur.fetchall()
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


    def add_subscriber(self, user_id, f_name, l_name, u_name, chat_id, chat_type, chat_title, status = 0):
        c_date = datetime.now()
        #Добавляем нового подписчика
        sql_query = """INSERT IGNORE INTO users
                       SET id_user     =  {0},
                           first_name  = '{1}',
                           last_name   = '{2}',
                           user_name   = '{3}',
                           create_date = '{4}'""".format(user_id,f_name,l_name,u_name,c_date)
        self.run_query(sql_query)

        #добавляем чат id
        sql_query = """INSERT IGNORE INTO users_chat
                       SET id_user     =  {0},
                           chat_id     =  {1},
                           chat_type   = '{2}',
                           create_date = '{3}',
                           chat_title  = '{4}'""".format(user_id, chat_id, chat_type, c_date, chat_title)
        self.run_query(sql_query)

        sql_query = """INSERT IGNORE INTO subscribe_users
                       SET id_user     =  {0},
                           id_status   =  {1},
                           create_date = '{2}'""".format(user_id,status,c_date)
        self.run_query(sql_query)


    def close(self):
        #Закрываем соединение с БД
        self.connection.close()