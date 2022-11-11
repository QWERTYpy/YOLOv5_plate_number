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
                                              (DATE TEXT NOT NULL,
                                              TIME TEXT NOT NULL,
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
        date_photo, time_photo, type_car, number_plate, number_plate_img, car_img = detect_data
        date_photo = f"'{date_photo}'"
        time_photo = f"'{time_photo}'"
        type_car = f"'{type_car}'"
        # number_plate = "'пусто'"
        if number_plate_img != "NULL":
            number_plate_img = f"'{number_plate_img}'"
        car_img = f"'{car_img}'"
        # Выполнение SQL-запроса для вставки данных в таблицу
        insert_query = f"INSERT INTO car_detection (DATE, TIME, TYPE, NUMBER, NUMBER_IMG, CAR_IMG) VALUES" \
                       f" ({str(date_photo)}, {str(time_photo)}, {type_car},{number_plate},{number_plate_img},{car_img})"
        self.cursor.execute(insert_query)
        self.connection.commit()
        print("1 запись успешно вставлена")



if __name__ == '__main__':
    bd = PostgessBase()
    # bd.create_table()
    dd = ["2022-11-11", "10.36.44", "22","22","22","22"]

    bd.insert_data(dd)




