import argparse
import configparser
import os
import shutil
from timeControl import testconnection as testcon

cfg = configparser.ConfigParser()
cfg.read('config.ini')

version_with_name = cfg['Info']['app'] + " " + cfg['Info']['ver']
foto_folder_path = str(cfg['General']['foto_folder_path'])
ftp_foto_folder_path = str(cfg['FTP']['ftp_foto_folder'])

cfg = configparser.ConfigParser()
cfg.read('config.ini')


# Функция для изменения конфигурации в файле
def update_config(section: str, option: str, value: str) -> None:
    """
    Обновляет значение параметра в файле конфигурации.

    Args:
        section (str): Название раздела в файле конфигурации.
        option (str): Название параметра в разделе.
        value (str): Новое значение параметра.

    Returns:
        None
    """
    # Создаем объект конфигурации
    config = configparser.ConfigParser()

    # Читаем конфигурационный файл
    config.read('config.ini')

    # Проверяем, существует ли секция, иначе создаем ее
    if section not in config:
        config[section] = {}

    # Обновляем значение параметра
    config[section][option] = str(value)

    # Записываем изменения обратно в файл
    with open('config.ini', 'w') as config_file:
        config.write(config_file)


def check_folder(path: str):
    """
    Проверяет количество файлов и общий вес файлов в папке.
    :param path: Путь к папке.
    """
    try:
        # Проверяем, существует ли папка
        if os.path.exists(path):
            files = os.listdir(path)
            total_files = len(files)
            total_size = sum(os.path.getsize(os.path.join(path, f)) for f in files)
            print(f"Путь: {path}")
            print(f"Количество файлов: {total_files}")
            if total_size > 1000:
                print(f"Общий размер: {total_size} байт")
            else:
                print("Общий размер: слишком маленький для беспокойства! ")
        else:
            print(f"Папка {path} не существует.")
    except Exception as e:
        print(f"Ошибка при проверке папки {path}: {e}")


def clear_folder(folder_path):
    """
    Удаляет все содержимое папки.
    :param folder_path: Путь к папке.
    """
    try:
        # Проверяем, существует ли папка
        if os.path.exists(folder_path):
            # Удаляем все файлы и подпапки из папки
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Ошибка при удалении {file_path}: {e}")
            print(f"Папка {folder_path} успешно очищена.")
        else:
            print(f"Папка {folder_path} не существует.")
    except Exception as e:
        print(f"Ошибка при очистке папки {folder_path}: {e}")


parser = argparse.ArgumentParser(description="Time Inspector 1.0 Учет рабочего времени\n"
                                             "с использованием api TimeControl, "
                                             "Все права защищены (с) 2024 \n"
                                             "Манукян Артур <it_doctor82@mail.ru>")

parser.epilog = ("Пример:\n"
                 "tminspector -d '156400' -o 'Название объекта'")

parser.add_argument('-v', '--version', action='version', version=version_with_name,
                    help='показать версию программы и выйти')
parser.add_argument('-d', '--door_id', help='Установить ID проходной')
parser.add_argument('-b', '--bot_token', help='Установить токен бота')
parser.add_argument('-f', '--check_folder', action='store_true', help='Проверка папки с фотографиями')
parser.add_argument('-cf', '--clear_folder', action='store_true', help='Очистить папку')
parser.add_argument('-t', '--testcon', action='store_true', help='Тест соединения')


# Разбор аргументов командной строки
args = parser.parse_args()

# Применение изменений к конфигурационному файлу
if args.door_id:
    update_config(args.door_id, 'TimeInspector', 'door_id')
if args.bot_token:
    update_config(args.bot_token, 'TimeInspector', 'bot_token')
if args.check_folder:
    check_folder(foto_folder_path)
    parser.exit()
if args.testcon:
    testcon()
    parser.exit()
if args.clear_folder:
    yesno = input("Вы уверены что хотите удалить все фотографии в папке?\n")
    if yesno == "Y" or "y" or "Д" or "д":
        clear_folder(foto_folder_path)
        check_folder(foto_folder_path)
        print("Папка 'Фото' успешно очищена")
        parser.exit()
    else:
        parser.exit()
