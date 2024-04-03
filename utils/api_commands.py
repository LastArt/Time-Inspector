import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')
tm_url = cfg['TimeControl']['tm_url']  # http://178.218.121.76:5053/api
pyrus_url = cfg['Pyrus']['pyrus_url']

# TIME CONTROL
# Перечень команд
GET_TEST = f"{tm_url}/testconnect"
GET_DEPARTAMENT = f"{tm_url}/department"  # Получить список отделов
GET_POSITION = f"{tm_url}/department"  # Получить список должностей
GET_WORKERS_ON_DEPARTAMENT = f"{tm_url}/persons?depart="  # Установить ID депортамента
GET_WORKERS_ON_POSITION = f"{tm_url}/persons?doljname="  # Установить по названию должности
GET_WORKERS_ON_TABNUM = f"{tm_url}/persons?TABNUM="
GET_ALL_WORKERS = f"{tm_url}/persons"
GET_WORKER_PHOTO = f"{tm_url}/persons/getfoto?userid="  # Установить ID пользователя
GET_FACT_EVENTS_ON_PERIOD = f"{tm_url}/fact_events?"  # startdate={START_DATE}&enddate={END_DATE}
GET_DOORID = f"{tm_url}/select?sql=select did from doors where code="
GET_DOORNAME = f"{tm_url}/select?sql=select * from doors where did="
GET_DESCIPLINE = f"{tm_url}/time/works?"
POST_WORKER_EVENT = f"{tm_url}/fact_events/add?"  # add?UID=

# PYRUS
# Перечень команд
