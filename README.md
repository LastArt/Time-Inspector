# ⏱ Time Inspector
Программа для автоматизации учета рабочего времени сотрудников на объектах строительства с использованием 
клиентского модуля TimeControl 
Подробнее про систему можно почитать на [сайте разработчика](https://www.time-control.ru/vozmojnosti/biometricheskie-sistemy/)  


### 📄 Описание
#### ⚠️ ВНИМАНИЕ! Программа находиться в глубокой ~~жопе~~ разработке, поэтому обновление описаний и инструкций будут дополняться по ходу пьесы. 
Программа использует [RestApi](https://www.time-control.ru/setup/docs/RestAPI.docx) системы TimeControl для получения информации о сотрудниках, событиях и учету времени. 
Так же при необходимости можно осуществлять запись в журналы Pyrus, GoogleSheet, Ftp. А все действия происходящие в системе фиксировать в виде уведомлений через телеграм бот.
В качестве основных рабочих модулей для регистрации и обработки используется одноплатный компьютер в связке с web камерой 
и HID считывателем
Принцип работы изображен на схеме:



![App Screenshot](https://i.imgur.com/jDlD4Ep.gif)


### 📎 Что потребуется для работы системы:
- [orange pi zero 3](https://market.yandex.ru/product--opi-zero-3/1892319347?sku=102084665336&uniqueId=17128978&do-waremd5=McPSjd9TAbqLzWk42W_pfg&sponsored=1)
- [считыватель](https://market.yandex.ru/product--st-ce011em-usb-schityvatel-smartec/992247710?sku=101359440552&uniqueId=892410&do-waremd5=HDc8Q-8ZrRYzR8m6UiYfKQ&sponsored=1) 
- python 3
- linux (arm)
- TimeControl в качестве основной системы учета рабочего времени


### 🚩 Флаги
Для более ясного понимания за что большинство флагов отвечает, читаем ниже в факе, а так же используем RestAPI TimeControl
```bash
-d  --door_id           установить\изменить id проходной
-t  --testcon           тест соединения c TimeControl
-b  --bot               токен тг бота для отправки уведомлений
-f  --folder            статус папки в которой храняться снимки с проходной 
-cf --clear-folder      очистить папку с снимками 
```
Функции программы в процессе постоянной доработки и оптимизации, поэтому будут актуализироваться.


### ⚙️ Конфигурационный файл
Вся программа работает на конфигурационном файле `config.ini`
Конфигурационный файл необходимо настроить перед запуском программы. В качестве примера внутри есть файл
config_example.ini (просто удалите _example и настройте его под себя)
#### Состав файла `config.ini`

```ini
[Info] # Общая информация (не требуется изменять)
app = TimeInspector
ver = 0.0.1
author = Manukian Artur
license = GPL

[General]
# Путь для хранения снимков с проходной
foto_folder_path = ./foto/
# Путь для хранения файла с логами
log_path = ./log.txt
# Включить/Выключить запись в журнал эксель
inner_journal_enabled = False
# Включить/Выключить работу через фтп (все файлы: журнал эксель, log.txt, и папка foto будут размещены на фтп)
ftp_enabled = False
# Включить/Выключить запись в Pyrus
pyrus_enabled = True
# Включить/Выключить уведомление в телеграм
tgbot_enabled = False
# Включить/Выключить запись в базу данных
database_enabled = True



[InnerJournal]
# Путь к файлу эксель
path_to_excel = ./file.xlsx

[FTP]
ftp_url = # URL ftp
ftp_login = # Логин ftp
ftp_password = # Пароль ftp
ftp_folder = # Корневая папка в которой будут размещаться файлы программы (log.txt, file.xlsx, папка foto)
ftp_foto_folder = # Папка в которую будут сохраняться снимки проходной
ftp_port = 21

[TimeControl]
tm_login = # логин от API (задается в клиенте TimeControl)
tm_password = # пароль от API (задается в клиенте TimeControl)
tm_url = # http://YOUR_IP:5053/api
door_id = # Устанавливаем ID проходной которую ранее создали в клиенте TimeControl


[Pyrus]
pyrus_bot_login = # Указываем логин созданного в pyrus-е бота
pyrus_bot_key = # Ключ бота
pyrus_url = https://api.pyrus.com/v4/


[TelegramBot]
tg_bot_token = # Укажите TOKEN телеграм бота который будет отправлять Вам уведомление
tg_id = # Укажите chat_id или id пользователя (можно получить через бот GetMyId https://t.me/getmyid_bot


[DataBase]
host = # Хост на котором размещена БД
database = # Название базы данных
user = # Пользователь
password = # Пароль
charset = utf8mb4
port = 3306

```
