import logging
import psycopg2
from bot.settings import (DATABASE, DBUSER, DBPASS, DBHOST, DBPORT)

class PostgreSQL:

    logging.basicConfig(level=logging.INFO)

    def __init__(self):
        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = psycopg2.connect(
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
                cur.execute(query) #выпоняем запрос
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

    def get_user_info(self, user_id):
        #Вытягиваем всю необходимую инфу о пользователе
        sql_query = "select * from telegram_users_tbl where id = {0}".format(user_id)

        result = self.run_query(sql_query)

        logging.info("Инфо о пользователе: " + str(result))

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


    def close(self):
        #Закрываем соединение с БД
        self.connection.close()