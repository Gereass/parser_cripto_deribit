# Парсер данных криптобиржи deribit.com по API

В данном репро предоставленно несколько скриптов, `parser_1.py`, парсит данные(index_price, timestamp) по 2м именам BTC-PERPETUAL и ETH-PERPETUAL и заносит их в БД.

Скрипт `parser_1_v2.py` осуществляет выборку всех идентификаторов имён btc_usd и eth_usd, затем парсит данные(index_price, timestamp) и заносит их в БД.

Скрипт `backend.py` - это FastApi клиент, с помощью которого можно получить доступ к спарсенным данным.
Чтобы запустить API, необходимо выполнить команду в терминале:

```console
uvicorn backend:app --host 0.0.0.0 --port 8000
```

Чтобы взаимодействовать с API, можно использовать любые HTTP-клиенты, такие как curl или библиотеки для работы с HTTP-запросами в Python, например, requests.

Примеры запросов:
Получение всех сохраненных данных по указанной валюте: `curl http://localhost:8000/get_all_data/?ticker=BTC-PERPETUAL`

Получение последней цены валюты: `curl http://localhost:8000/get_last_price/?ticker=BTC-PERPETUAL`

Получение цены валюты с фильтром по дате: `curl http://localhost:8000/get_price_by_date/?ticker=BTC-PERPETUAL&date=1730631356834`

Примечание: перед запуском API необходимо установить env и все необходимые зависимости из файла `requirements.txt`, а так же спарсить данные выполнив `parser_1.py` или `parser_1_v2.py`, на своё усмотрени, для создания БД.

Создать и  активировать вирт. окружение, а так же установить зависимости можно с помощью:

```console
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```  

В файле `Backend_dev_test.pdf` предоставлен текст с подробным описанием тестового задания.