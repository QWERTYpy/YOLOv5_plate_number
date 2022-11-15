# pass: 12345
# port: 5432

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

class PostgessBase:
    def __init__(self):
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="12345",
                                          host="127.0.0.1",
                                          port="5432")
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
            # Создаем базу данных, к которой будем подключаться, если она не существует
            self.cursor.execute("SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = 'car_python_db'")
            not_exists, = self.cursor.fetchone()
            if not_exists:
                self.cursor.execute('CREATE DATABASE car_python_db')
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Первичное соединение с PostgreSQL закрыто")
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="12345",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="car_python_db")
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
            # Создаем таблицу, если она не существует
            create_table_query = '''CREATE TABLE if not exists car_detection
                                              (PLACE TEXT NOT NULL,
                                              DATE DATE NOT NULL,
                                              TIME TIME NOT NULL,
                                              TYPE TEXT NOT NULL,
                                              NUMBER TEXT,
                                              NUMBER_IMG TEXT,
                                              CAR_IMG TEXT); '''
            # Выполнение команды: это создает новую таблицу
            self.cursor.execute(create_table_query)
            self.connection.commit()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Соединение с PostgreSQL закрыто")



    def insert_data(self, detect_data):
        """
        Вставка данных в БД
        :param detect_data:
        :return:
        """
        date_photo, time_photo, type_car, number_plate, number_plate_img, car_img = detect_data
        place = "'Корд'"
        date_photo = f"'{date_photo}'"
        time_photo = f"'{time_photo.replace('.',':')}'"
        type_car = f"'{type_car}'"
        # number_plate = "'пусто'"
        if number_plate_img != "NULL":
            number_plate_img = f"'{number_plate_img}'"
        car_img = f"'{car_img}'"
        # Выполнение SQL-запроса для вставки данных в таблицу
        insert_query = f"INSERT INTO car_detection (PLACE, DATE, TIME, TYPE, NUMBER, NUMBER_IMG, CAR_IMG) VALUES" \
                       f" ({place}, {str(date_photo)}, {str(time_photo)}, {type_car},{number_plate},{number_plate_img},{car_img})"
        self.cursor.execute(insert_query)
        self.connection.commit()
        # print("1 запись успешно вставлена")

    def date_exists(self, date_dir):
        """
        Функция проверяет существуют ли записи с определенной датой, чтобы не обрабатывать папки дважды.
        :param date_dir:
        :return: True or False
        """
        insert_query = f"SELECT EXISTS (SELECT * FROM public.car_detection WHERE date = '{date_dir}');"
        self.cursor.execute(insert_query)
        return self.cursor.fetchall()[0][0]

    def time_exists(self, date_dir):
        """
        Поиск максимального времени на указанную дату
        :param date_dir: интересующая дата
        :return: максимальное время
        """
        insert_query = f"select max(TIME) from public.car_detection WHERE date = '{date_dir}'"
        self.cursor.execute(insert_query)
        max_time = self.cursor.fetchall()
        return max_time[0][0]

        # insert_query = f"SELECT EXISTS (SELECT * FROM public.car_detection WHERE date = '{date_dir}');"
        # self.cursor.execute(insert_query)
        # return self.cursor.fetchall()[0][0]

    def select_date(self, data_search, time_search_low, time_search_hight, type_search):
        """
        Выбор данных из БД по дате, времени и типу транспортного средства
        :param data_search: дата поиска
        :param time_search_low: с какого времени
        :param time_search_hight: по какое время
        :param type_search: тип транспортного средства
        :return: Список найденных строк
        """
        if type_search == "Все":
            insert_query = f"select * from public.car_detection where date = " \
                           f"'{data_search}' and time  between '{time_search_low}' and '{time_search_hight}'"
        else:
            insert_query = f"select * from public.car_detection where date = " \
                       f"'{data_search}' and time  between '{time_search_low}' and '{time_search_hight}' and " \
                       f"type = '{type_search}'"
        self.cursor.execute(insert_query)
        return self.cursor.fetchall()


    def all_date(self):
        """
        Поиск всех дат, на которые есть данные
        :return:
        """
        insert_query = f"select distinct date from public.car_detection"
        self.cursor.execute(insert_query)
        return self.cursor.fetchall()

    def mm_date(self):
        """
        Функция выдает минимальную и макисмальную дату в БД
        :return: Возвращаяет список с мин и макс датой
        """
        insert_query = f"select min(DATE), max(DATE) from public.car_detection"
        self.cursor.execute(insert_query)
        return self.cursor.fetchall()

    def del_duplicate(self):
        """
        Удаление дубликатов строк
        :return:
        """
        # insert_query = f"SELECT(public.car_detection. *)::text, count(*) FROM public.car_detection GROUP " \
        #                f"BY public.car_detection. * HAVING count(*) > 1"

        # insert_query = f"SELECT  unnest(ctids[2:]) FROM" \
        #                f"  (SELECT array_agg(ctid) ctids " \
        #                f"FROM public.car_detection T GROUP BY T::text ) T"
        insert_query = """
        DELETE FROM
            public.car_detection
        WHERE
            ctid = ANY(ARRAY(
                SELECT
                    unnest(ctids[2:])
                FROM
                    (
                    SELECT
                        array_agg(ctid) ctids
                    FROM
                        public.car_detection T
                    GROUP BY
                        T::text
                    ) T
            )::tid[])
        """
        self.cursor.execute(insert_query)
        #return self.cursor.fetchall()


if __name__ == '__main__':
    bd = PostgessBase()
    # bd.create_table()
    # dd = ["2022-11-10", "10:36:44", "22","22","22","22"]
    # print(bd.select_date("2022-11-10", "02:00:00","06:00:00"))
    #bd.insert_data(dd)
    # print(bd.time_exists("2022-11-10"))
    print(bd.del_duplicate())



