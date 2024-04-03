from colorama import Back
from utils.globalvars import not_valid_data
from utils.servicefunc import *
from timeControl import *
from pyrus import *
from camera import *
from tgbot import *
from innerjournal import *
from db import *

log = Minilog()

cfg = configparser.ConfigParser()
cfg.read('config.ini')


def main():
    welcome_screen()
    while True:
        input_result = input(Fore.MAGENTA + "Программа ожидает ввода данных ----> " + Fore.RESET + Back.RESET)
        log.write_start()
        room_info = get_door_info()
        uid = get_uid(input_result)
        if uid is None:
            print(Fore.RED + not_valid_data + Fore.WHITE)
        else:
            access_token = get_access_token(login=cfg['Pyrus']['pyrus_bot_login'],
                                            security_key=cfg['Pyrus']['pyrus_bot_key'])
            foto = make_capture()
            guid = upload_file(file_path=foto, access_token=access_token)
            event_data = add_event(uid=uid[0], roomid=room_info)
            discipline_status: dict = get_discipline(uid=uid[0])
            current_time = current_time_in_timezone()
            if event_data['ADD_RESULT'] == "1":
                if cfg['General']['pyrus_enabled'] == "True":
                    task_id = add_in_pyrus_journal(uid=uid[0],
                                                   fio=uid[1],
                                                   doljnost=uid[2],
                                                   roomname=room_info[1],
                                                   status="🟢 Приход",
                                                   data=str(dt.now().strftime('%Y-%m-%d')),
                                                   time=current_time,
                                                   foto_guid=guid,
                                                   foto_path=foto,
                                                   token=access_token,
                                                   discipline_status=discipline_status)
                    attache_file(task_id=task_id['task']['id'], foto_guid=guid, access_token=access_token)
                if cfg['General']['inner_journal_enabled'] == "True":
                    add_to_excel(uid=uid[0],
                                 fio=uid[1],
                                 doljnost=uid[2],
                                 roomname=room_info[1],
                                 status="🟢 Приход",
                                 data=str(dt.now().strftime('%Y-%m-%d')),
                                 time=current_time,
                                 foto_path=foto,
                                 discipline_status=discipline_status,
                                 excel_file=cfg['InnerJournal']['path_to_excel'])
                if cfg['General']['ftp_enabled'] == "True":
                    pass
                if cfg['General']['tgbot_enabled'] == "True":
                    # Установить проверку на опоздания и ранние уходы и 2 типа ссообщений отпавлять с и без
                    send_message_and_foto_telegram_bot(foto, f"🟢 Приход\n"
                                                             f"{datetimeNow} в {current_time}\n{uid}")
                if cfg['General']['database_enabled'] == "True":
                    add_to_database(uid=uid[0],
                                    fio=uid[1],
                                    doljnost=uid[2],
                                    roomname=room_info[1],
                                    status="🟢 Приход",
                                    data=str(dt.now().strftime('%Y-%m-%d')),
                                    time=current_time,
                                    foto=read_image_as_bytes(foto),
                                    discipline_status=discipline_status)
                if cfg['General']['googlesheets_enabled'] == "True":
                    pass
            elif event_data['ADD_RESULT'] == "2":
                if cfg['General']['pyrus_enabled'] == "True":
                    task_id = add_in_pyrus_journal(uid=uid[0],
                                                   fio=uid[1],
                                                   doljnost=uid[2],
                                                   roomname=room_info[1],
                                                   status="🔴 Уход",
                                                   data=str(dt.now().strftime('%Y-%m-%d')),
                                                   time=current_time,
                                                   foto_guid=guid,
                                                   foto_path=foto,
                                                   token=access_token,
                                                   discipline_status=discipline_status)
                    attache_file(task_id=task_id['task']['id'], foto_guid=guid, access_token=access_token)
                if cfg['General']['inner_journal_enabled'] == "True":
                    add_to_excel(uid=uid[0],
                                 fio=uid[1],
                                 doljnost=uid[2],
                                 roomname=room_info[1],
                                 status="🔴 Уход",
                                 data=str(dt.now().strftime('%Y-%m-%d')),
                                 time=current_time,
                                 foto_path=foto,
                                 discipline_status=discipline_status,
                                 excel_file=cfg['InnerJournal']['path_to_excel'])
                if cfg['General']['ftp_enabled'] == "True":
                    pass
                if cfg['General']['tgbot_enabled'] == "True":
                    send_message_and_foto_telegram_bot(foto, f"🔴 Уход\n"
                                                             f"{str(dt.now().strftime('%Y-%m-%d'))} в "
                                                             f"{current_time}\n{uid}")
                if cfg['General']['database_enabled'] == "True":
                    add_to_database(uid=uid[0],
                                    fio=uid[1],
                                    doljnost=uid[2],
                                    roomname=room_info[1],
                                    status="🔴 Уход",
                                    data=str(dt.now().strftime('%Y-%m-%d')),
                                    time=current_time,
                                    foto=read_image_as_bytes(foto),
                                    discipline_status=discipline_status)
                if cfg['General']['googlesheets_enabled'] == "True":
                    pass
            elif event_data['ADD_RESULT'] == "3":
                if cfg['General']['pyrus_enabled'] == "True":
                    task_id = add_in_pyrus_journal(uid=uid[0],
                                                   fio=uid[1],
                                                   doljnost=uid[2],
                                                   roomname=room_info[1],
                                                   status="⚠️ Отметка уже есть",
                                                   data=str(dt.now().strftime('%Y-%m-%d')),
                                                   time=current_time,
                                                   foto_guid=guid,
                                                   foto_path=foto,
                                                   token=access_token,
                                                   discipline_status=discipline_status)
                    attache_file(task_id=task_id['task']['id'], foto_guid=guid, access_token=access_token)
                if cfg['General']['inner_journal_enabled'] == "True":
                    add_to_excel(uid=uid[0],
                                 fio=uid[1],
                                 doljnost=uid[2],
                                 roomname=room_info[1],
                                 status="️ Отметка уже есть",
                                 data=str(dt.now().strftime('%Y-%m-%d')),
                                 time=current_time,
                                 foto_path=foto,
                                 discipline_status=discipline_status,
                                 excel_file=cfg['InnerJournal']['path_to_excel'])
                if cfg['General']['ftp_enabled'] == "True":
                    pass
                if cfg['General']['tgbot_enabled'] == "True":
                    send_message_to_telegram_bot(f"⚠️ Отметка уже есть\n"
                                                 f"{str(dt.now().strftime('%Y-%m-%d'))} в {current_time}\n{uid}")
                if cfg['General']['database_enabled'] == "True":
                    add_to_database(uid=uid[0],
                                    fio=uid[1],
                                    doljnost=uid[2],
                                    roomname=room_info[1],
                                    status="⚠️ Отметка уже есть",
                                    data=str(dt.now().strftime('%Y-%m-%d')),
                                    time=current_time,
                                    foto=read_image_as_bytes(foto),
                                    discipline_status=discipline_status)
                if cfg['General']['googlesheets_enabled'] == "True":
                    pass
        log.write_finish()


if __name__ == '__main__':
    main()
