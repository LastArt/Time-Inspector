import requests
import json
from utils.servicefunc import minute_to_timeformat
from minilog import Minilog

log = Minilog()


def get_access_token(login, security_key):
    url = "https://api.pyrus.com/v4/auth"
    headers = {"Content-Type": "application/json"}
    data = {
        "login": login,
        "security_key": security_key
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        log.write_error(f"Ошибка в функции get_access_token -> {response.text}, возвращаем None")
        return None


def get_form_on_task(access_token: str):  # task_id: str,
    url = f"https://api.pyrus.com/v4/forms"  # /{task_id}
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        beauty = json.dumps(response.json(), indent=2, ensure_ascii=False)
        with open('forms.txt', 'a', encoding='utf-8') as file:
            file.write(str(beauty))
        return response.json()
    else:
        log.write_error(f"Ошибка в функции get_form_on_task -> {response.text}, возвращаем None")
        return None


def upload_file(file_path: str, access_token: str):
    """
    Загружает файл на сервер Pyrus и возвращает его GUID.

    Параметры:
        file_path (str): Путь к файлу для загрузки.
        access_token (str): Токен доступа для аутентификации.

    Возвращает:
        str: GUID загруженного файла, если загрузка прошла успешно, в противном случае None.
    """
    url = "https://api.pyrus.com/v4/files/upload"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        with open(file_path, "rb") as file:
            files = {
                "file": (file_path.split("/")[-1], file, "application/octet-stream")
            }
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                print("UPLOAD DATA ", response.json())
                return response.json().get("guid")
            else:
                log.write_error(f"(upload_file): Ошибка при загрузке файла. Код ответа: {response.status_code}")
                print(f"Ошибка при загрузке файла. Код ответа: {response.status_code}")
                return None
    except FileNotFoundError:
        log.write_error("(upload_file): Файл не найден.")
        print("Файл не найден.")
        return None
    except Exception as e:
        log.write_error(f"(upload_file): Произошла ошибка: {e}")
        print(f"Произошла ошибка: {e}")
        return None


def add_in_pyrus_journal(uid: str, fio: str, doljnost: str, roomname: str, status: str, data: str, time: str,
                         token: str, discipline_status: dict):
    """
            Создает новую задачу в системе Pyrus и прикрепляет к ней фотографию.
            Параметры:
                uid (str): UID сотрудника.
                fio (str): ФИО сотрудника.
                doljnost (str): Должность сотрудника.
                roomname (str): Название помещения.
                status (str): Статус (приход/уход).
                data (str): Дата.
                time (str): Время.
                token (str): Токен доступа API
                foto_guid (str): GUID загруженной фотографии.
                access_token (str): Токен доступа для аутентификации.
                :param discipline_status:
            """
    url = "https://api.pyrus.com/v4/tasks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    if discipline_status['opoz'] != "0":
        opozdanie = minute_to_timeformat(discipline_status['opoz'])
    else:
        opozdanie = "-"
    if discipline_status['rann'] != "0":
        ran_uhod = minute_to_timeformat(discipline_status['rann'])
    else:
        ran_uhod = "-"
    if discipline_status['prog'] != "0":
        progul = discipline_status['prog']
    else:
        progul = "-"
    if discipline_status['zade'] != "0":
        zaderjka = minute_to_timeformat(discipline_status['zade'])
    else:
        zaderjka = "-"
    body = {
        "form_id": 1418523,
        "fields": [
            {"id": 1, "value": uid},
            {"id": 2, "value": fio},
            {"id": 16, "value": doljnost},
            {"id": 17, "value": roomname},
            {"id": 18, "value": status},
            {"id": 8, "value": data},
            {"id": 19, "value": time},
            {"id": 13, "value": opozdanie},
            {"id": 14, "value": ran_uhod},
            {"id": 15, "value": progul},
            {"id": 20, "value": zaderjka}
        ]
    }
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error-->(add_in_pyrus_journal):", response.text)
        return None


def attache_file(task_id, foto_guid, access_token):
    url = f'https://api.pyrus.com/v4/tasks/{task_id}/comments'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'attachments': [
            {'guid': foto_guid}
        ]
    }
    print("guid in attache", foto_guid)
    print("Task id - ", task_id)
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Удачно загрузили фото в Pyrus!")
        return response.json()
    else:
        print(f"Failed to upload comment with file. Status code: {response.status_code}")
        return None
