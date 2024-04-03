import cv2
import configparser
from datetime import datetime as dt
from minilog import Minilog

cfg = configparser.ConfigParser()
cfg.read('config.ini')

log = Minilog()


def make_capture(quality=90, exposure=5):
    """
    Захватывает снимок отметившегося на проходной.
    :param quality: Качество JPEG (от 0 до 100). Значение по умолчанию - 90.
    :param exposure: Уровень экспозиции камеры (от 0 до 1). Значение по умолчанию - 0.8.
    :return:
        str: Путь к сохраненному снимку.
    """
    try:
        # Открыть видеопоток с камеры
        cap = cv2.VideoCapture(0)  # 0 указывает на использование первой доступной камеры
        # Проверка, успешно ли открыт видеопоток
        if not cap.isOpened():
            print("Ошибка: не удалось открыть видеопоток")
            exit()
        # Установка параметров камеры
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        # Считать кадр с камеры
        ret, frame = cap.read()
        # Проверка, успешно ли считан кадр
        if not ret:
            log.write_error("Ошибка: не удалось считать кадр")
            print("Ошибка: не удалось считать кадр")
            exit()
        # Проверка условия на Локальное сохранение или FTP
        filename = f"{cfg['General']['foto_folder_path']}snapshot_{str(dt.now().strftime('%Y-%m-%d_%H_%M_%S'))}.jpeg"
        cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        print(f"Фотография сохранена локально: {filename}")
        log.write_log(f"make_capture(): Make snapshot from camera - {filename}")
        cv2.destroyAllWindows()
        cap.release()
        return filename
    except Exception as e:
        log.write_error(f'make_capture(): {e}')
