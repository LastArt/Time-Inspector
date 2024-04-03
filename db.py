import pymysql
import configparser
from utils.servicefunc import minute_to_timeformat
from minilog import Minilog

log = Minilog()

cfg = configparser.ConfigParser()
cfg.read('config.ini')

db_params = {
    'host': cfg['DataBase']['host'],
    'user': cfg['DataBase']['user'],
    'password': cfg['DataBase']['password'],
    'database': cfg['DataBase']['database'],
    'port': int(cfg['DataBase']['port'])  # Необязательный параметр, по умолчанию 3306
}


def add_to_database(uid: str, fio: str, doljnost: str, roomname: str, status: str, data: str, time: str,
                    foto: str, discipline_status: dict):
    """
    Записывает переданные значения в базу данных MySQL.

    Параметры:
        uid (str): UID сотрудника.
        fio (str): ФИО сотрудника.
        doljnost (str): Должность сотрудника.
        roomname (str): Название проходной.
        status (str): Статус (приход/уход).
        data (str): Дата.
        time (str): Время.
        foto (str): Фотография в виде байтов.
        discipline_status: dict: Информация об опозданиях, ранних уходах, прогулах и задержках.
        db_params (dict): Параметры подключения к базе данных MySQL в формате:
                          {
                              'host': 'адрес_хоста',
                              'user': 'пользователь',
                              'password': 'пароль',
                              'database': 'название_базы_данных',
                              'port': 'порт_базы_данных' (необязательно, по умолчанию 3306)
                          }
    """
    try:
        # Установка соединения с базой данных
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()

        if int(discipline_status['opoz']) != 0:
            opozdanie = minute_to_timeformat(discipline_status['opoz'])
        else:
            opozdanie = "00:00"
        if int(discipline_status['rann']) != 0:
            ran_uhod = minute_to_timeformat(discipline_status['rann'])
        else:
            ran_uhod = "00:00"
        if int(discipline_status['prog']) != 0:
            progul = discipline_status['prog']
        else:
            progul = "0"
        if int(discipline_status['zade']) != 0:
            zaderjka = minute_to_timeformat(discipline_status['zade'])
        else:
            zaderjka = "00:00"

        # Создание запроса SQL для вставки данных
        sql = """INSERT INTO worktime (uid, fio, doljnost, roomname, status, dateOfWork, timeOfWork,  foto,
                 opozdanie, ranniyUhod, zaderjka, progul) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        # Выполнение запроса SQL
        cursor.execute(sql, (uid, fio, doljnost, roomname, status, data, time, foto, opozdanie, ran_uhod, progul,
                             zaderjka))
        # Зафиксировать изменения в базе данных
        conn.commit()
        conn.close()
        log.write_log("(add_to_database): Данные успешно записаны в базу данных!")
    except Exception as e:
        log.write_error(f"(add_to_database): Ошибка при работе с базой данных:{e}")
