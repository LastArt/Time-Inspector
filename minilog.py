from datetime import datetime as dt


class Minilog:
    """
    Класс для записи логов в файл.

    Attributes:
        file_name (str): Имя файла логов.
    """

    def __init__(self, file_name='log.txt'):
        """
        Конструктор класса Logger.

        Args:
            file_name (str, optional): Имя файла логов. По умолчанию 'log.txt'.
        """
        self.file_name = file_name

    def set_file_name(self, file_name):
        """
        Метод для изменения имени файла логов.

        Args:
            file_name (str): Новое имя файла логов.
        """
        self.file_name = file_name

    def write_error(self, event:str):
        """
        Метод для записи ошибки в файл логов.

        Args:
            event (str): Описание ошибки.
        """
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'🆘ERROR_{str(dt.now().strftime("%Y-%m-%d_%H_%M_%S"))}:{event}\n')

    def write_warning(self, event:str):
        """
        Метод для записи предупреждения в файл логов.

        Args:
            event (str): Описание предупреждения.
        """
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'⚠️WARNING_{str(dt.now().strftime("%Y-%m-%d_%H_%M_%S"))}:{event}\n')

    def write_start(self):
        """
        Метод для записи метки начала в файл логов.
        """
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'🚀START-----{str(dt.now().strftime("%Y-%m-%d_%H_%M_%S"))}--------\n\n')

    def write_finish(self):
        """
        Метод для записи метки завершения в файл логов.
        """
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'\n🏁FINISH-----{str(dt.now().strftime("%Y-%m-%d_%H_%M_%S"))}--------\n\n')

    def write_log(self, event:str):
        """
        Метод для записи общего лога в файл логов.

        Args:
            event (str): Описание события.
        """
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'ℹ️LOG :{str(dt.now().strftime("%Y-%m-%d_%H_%M_%S"))}: {event}\n')

    def change_file_name(self, new_file_name):
        """
        Метод для изменения имени файла логов.

        Args:
            new_file_name (str): Новое имя файла логов.
        """
        self.set_file_name(new_file_name)