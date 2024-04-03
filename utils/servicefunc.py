from colorama import Fore
from utils.globalvars import welcome, logo_time, logo_inspector, inspector
from datetime import datetime as dt
import pytz
from minilog import Minilog

log = Minilog()

dateNow = dt.now().strftime('%d.%m.%y')
timeNowS = str(dt.now().strftime("%H_%M"))
timeNowF = str(dt.now().strftime("%H_%M_%S"))
datetimeNow = str(dt.now().strftime("%Y-%m-%d_%H_%M_%S"))


def welcome_screen():
    print(Fore.YELLOW + inspector + Fore.RESET)
    print(Fore.BLUE + logo_time + Fore.GREEN + logo_inspector)
    print(Fore.YELLOW + "", welcome)


def current_time_in_timezone(timezone_name='Europe/Moscow'):
    """
    Функция возвращает текущее время в указанном часовом поясе.

    :param timezone_name: название часового пояса, по умолчанию 'Europe/Moscow'
    :return: текущее время в формате 'часы:минуты'
    """
    desired_timezone = pytz.timezone(timezone_name)
    current_time = dt.now(desired_timezone)
    return current_time.strftime('%H:%M')


def minute_to_timeformat(minute: str) -> str:
    if int(minute) < 60:
        return minute
    else:
        h = int(minute) // 60
        m = int(minute) % 60
        return "{:02d}:{:02d}".format(h, m)


def read_image_as_bytes(file_path):
    try:
        with open(file_path, 'rb') as file:
            image_bytes = file.read()
            return image_bytes
    except FileNotFoundError:
        log.write_error(f"Произошла ошибка в функции {read_image_as_bytes}: Файл изображения не найден")
        return None
    except Exception as e:
        log.write_error(f"Произошла ошибка в функции {read_image_as_bytes}: {e}")
        return None
