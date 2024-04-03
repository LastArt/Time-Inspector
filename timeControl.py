import requests
from utils.api_commands import *
from utils.servicefunc import *
from utils.globalvars import acces_denied, acces_accepted

cfg = configparser.ConfigParser()
cfg.read('config.ini')
username = cfg['TimeControl']['tm_login']
password = cfg['TimeControl']['tm_password']

log = Minilog()


def testconnection():
    try:
        response = requests.get(GET_TEST, auth=(username, password))
        if response.status_code == 200:
            print(f"Соединение установлено (Код -" + Fore.GREEN + f"{response.status_code})" + Fore.RESET)
            return response.json()
        else:
            print(f"Соединение не установлено (Код -" + Fore.RED + f"{response.status_code})" + Fore.RESET)
            return response.json()
    except Exception as e:
        log.write_error(f'testcon(): {e}')


def get_uid(cardname: str):
    try:
        response = requests.post(GET_WORKERS_ON_TABNUM + cardname, auth=(username, password))
        if response.status_code == 200:
            data = response.json()
            uid: str = data['data'][0]['UID']
            fulname: str = data['data'][0]['FULLNAME']
            doljnost: str = data['data'][0]['DOLJNAME']
            log.write_log(f'get_uid(): Выполнен запрос - {response.url} с статусом {str(response.status_code)}\n'
                          f'Получено: UID={uid}')
            return uid, fulname, doljnost
    except Exception as e:
        log.write_error(f'get_uid(): {e}')


def get_door_info():
    try:
        response = requests.post(GET_DOORID + cfg['TimeControl']['door_id'], auth=(username, password))
        if response.status_code == 200:
            data = response.json()
            res = data['data'][0]['DID']
            subresponse = requests.post(GET_DOORNAME + res, auth=(username, password))
            if subresponse.status_code == 200:
                data = subresponse.json()
                door_name = data['data'][0]['DOORNAME']
                log.write_log(f'get_door_info(): Выполнен запрос - {response.url} с '
                              f'статусом - {str(response.status_code)}\n Получено: DID={res}--DOORNAME={door_name}')
                return res, door_name
            else:
                door_name = "Проходная не определена"
                log.write_log(f'get_door_info(): Выполнен запрос - {response.url} с '
                              f'статусом - {str(response.status_code)}\n Получено: DID={res}--DOORNAME={door_name}')
                return res, door_name
    except Exception as e:
        log.write_error(f'get_door_id(): {e}')


def add_event(uid: str, roomid: str):
    if uid is not None:  # Измененное условие:
        params = {
            "uid": uid,
            "doorid": roomid[0],
            "useforfact": "1",
            "regmetod": "2"
        }
        try:
            response = requests.post(POST_WORKER_EVENT, data=params, auth=(username, password))
            if response.status_code == 200:
                log.write_log(f'Выполнен запрос - {response.url} с статусом {str(response.status_code)}\n'
                              f'Получено: {str(response.json())}')
                print(Fore.GREEN + acces_accepted + Fore.WHITE)
                return response.json()
        except Exception as e:
            log.write_error(f'add_event(): {e}')
    else:
        print(Fore.RED + acces_denied + Fore.WHITE)
        log.write_warning(f"add_event: Доступ по UID [{uid}] невозможен!")


def get_discipline(uid: str) -> dict:
    try:
        url = f"{GET_DESCIPLINE}startdate={datetimeNow}&enddate={datetimeNow}&person_list={uid}"

        print("URL = ", url)
        response = requests.post(url, auth=(username, password))
        if response.status_code == 200:
            data = response.json()
            opozdanie: str = data['data'][0]['OPOZD']
            zaderjka: str = data['data'][0]['ZADERJ']
            rannii_uhod: str = data['data'][0]['EARLY_OUT']
            progul: str = data['data'][0]['PROGUL']
            log.write_log(f'get_uid(): Выполнен запрос - {response.url} с статусом {str(response.status_code)}\n'
                          f'Получено: UID={uid}')
            return {"opoz": opozdanie,
                    "zade": zaderjka,
                    "rann": rannii_uhod,
                    "prog": progul}
    except Exception as e:
        log.write_error(f'get_uid(): {e}')
