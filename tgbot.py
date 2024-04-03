import requests
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')
telegram_token = cfg['TelegramBot']['tg_bot_token']
telegram_chat_id = cfg['TelegramBot']['tg_id']

def send_message_to_telegram_bot(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    params = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(url, json=params)
    return response.json()

def send_message_and_foto_telegram_bot(photo_path: str, caption=None):
    print("File PATH = ", photo_path)
    url = f"https://api.telegram.org/bot{telegram_token}/sendPhoto"
    files = {"photo": open(photo_path, "rb")}
    data = {"chat_id": telegram_chat_id, "caption": caption}
    response = requests.post(url, files=files, data=data)
    return response.json()
