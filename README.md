# Тестовое задание по Backend-разработке сервиса IP-телефонии #

## Содержание ##

[1. Условия задания](#условия-задания)    
[2. Описание решения](#описание-решения)    
[3. Результат](#результат)    
[4. Инструкция по запуску проекта](#инструкция-по-запуску-проекта)    
[5. Мысли про SIP](#мысли-про-sip)    

## Условия задания ##

Разработать бэкенд сервиса, осуществляющего автоматический дозвон до загружаемой
пользователем базы абонентов и воспроизводящий при дозвоне загруженный звуковой
файл.

У пользователя должна быть возможность задать параметры подключения к поставщику
телефонии (адрес sip шлюза, имя пользователя, пароль, etc.), загрузить звуковой
файл, загрузить базу абонентов (список телефонных номеров) и инициировать дозвон
до базы абонентов с воспроизведение загруженного звукового файла.

Требования к сервису:

1. Аутентификация OAuth 2.0 с идентификацией по логину/паролю
2. Авторизация запроса токеном в заголовке
3. RESTfull API + swagger для тестирования
4. Реализация телефонного дозвона без привлечения сторонних сервисов.

[:arrow_up: Содержание](#содержание)

----

## Описание решения ##

- Для запуска и демонстрации работы API решено использовать вместо **`Django`**
и **`PostgreSQL`** более легковесные и подходящие для тестовых задач web-сервер
**`Bottle`** и СУБД **`SQLite3`**.

- Тестовая база данных **`SQLite3`** содержит две таблицы. В таблице **`Users`**
хранятся пользовательские данные, в таблице **`Callbase`**&nbsp;&mdash; база
абонентов.

### Таблица Users ###

    uid         VARCHAR(36)     (PRIMARY KEY) в формате uuid4
    name        VARCHAR(1024)   Имя
    login       VARCHAR(1024)   Логин
    password    VARCHAR(1024)   Пароль
    acc_token   VARCHAR(1024)   Access-токен с ограниченным временем действия
    expired     FLOAT           Дата окончания действия access-токена в UNIX-формате
    comment     TEXT(1024)      Дополнительная информация

### Таблица Callbase ###

    cid         VARCHAR(36)     (PRIMARY KEY) в формате uuid4
    name        VARCHAR(1024)   Имя
    number      VARCHAR(12)     Номер телефона
    comment     TEXT(1024)      Дополнительная информация

- Для авторизованного доступа используется **JSON Web Token (JWT)**.

- Валидация входных данных (логин, пароль, другие запросы), кроме access-токена
не проводится.

- В будущем можно расширить функционал применением refresh-токена, который
клиент должен использовать в запросе на обновление при истечении срока действия
access-токена. Однако сейчас при просроченном access-токене надо заново
логиниться на сервере и получать новый access-токен (ещё на 10&nbsp;минут).

[:arrow_up: Содержание](#содержание)

----

## Результат ##

[**`main.py`**](main.py)&nbsp;&mdash; Web-сервер **`Bottle`**. Доступ по
[http://localhost:8080](http://localhost:8080). Содержит декларации требуемых
ресурсов, необходимый функционал которых вынесен в отдельный модуль
**`api_srv.py`**.

[**`api_srv.py`**](api_srv.py)&nbsp;&mdash; модуль с методами API, необходимыми
для работы сервера.

[**`sqlite/script.sql`**](sqlite/script.sql)&nbsp;&mdash; скрипт для создания
начальной базы данных `sqlite/db.sqlite3` для **SQLite** (три пользователя и три
абонента).

Ресурс `/srv1/auth/login` под HTTP-метод POST&nbsp;&mdash; для аутентификации.
Принимает json с логином/паролем, проверяет по базе пользователей, генерит
access-токен и время его действия, заносит их в базу и выдаёт клиенту в обратном
json.

Ресурс `/srv1/abon/all` под HTTP-метод GET&nbsp;&mdash; для выдачи всей базы
телефонных абонентов. Здесь уже требуется авторизованный доступ. Принимает JWT
(через декоратор) распаковывает, из `header` достаёт access-токен, проверяет и
при положительном результате проверки возвращает json с базой.

Точнее так: для удобства авторизации создан универсальный декоратор для методов
GET/POST, в который вынесены распаковка JWT ключом из константы `JWT_KEY`,
извлечение access-токена из `header`, &laquo;пробивка по базе&raquo; передача в
декорируемый метод результата проверки и самого запроса из `payload`.

**Таким образом создана основа для создания любых других требуемых ресурсов с
HTTP-методами GET или POST, с аутентификацией или без неё.**

Ресурс `/srv1/call/sample`&nbsp;&mdash; делает тестовый звонок (не реализован,
только заглушка).

[**`api_client.py`**](api_client.py)&nbsp;&mdash; Консольная версия RESTful API
для тестирования API сервера.

Глобальная константа `JWT_KEY` должна быть одинаковой в `api_srv.py` и в
`api_client.py` для успешной упаковки и распаковки JWT.

При создании любых новых ресурсов на сервере, требующих авторизованного доступа,
и методов их тестирования на клиенте должны отправлять/принимать JWT в ключе
`req_data`.

[:arrow_up: Содержание](#содержание)

----

## Инструкция по запуску проекта ##

1. На компьютере должен быть установлен **Python** не слишком старой версии
(например, **3.8** или более поздней) и соответствующий пакетный менеджер
**pip**.
2. Установить **SQLite3** можно по руководствам
[для Linux](https://linoxide.com/install-use-sqlite-linux) или
[для Windows](https://www.sqlitetutorial.net/download-install-sqlite/). Хотя для
работы под Windows всё необходимое для работы уже есть в директории
[`sqlite`](sqlite).
3. Скачать файлы проекта из текущей директории репозитория в локальную
директорию компьютера.
4. Для создания файла БД `sqlite/db.sqlite3` войти в директорию
[`sqlite`](sqlite), запустить **SQLite** и потом ввести мета-команды:

    ```bash
    # Запуск
    sqlite3 db.sqlite3

    # Мета-команды
    .read script.sql
    .exit
    ```

5. Примерная последовательность команд в консоли терминала для запуска сервера
в виртуальном окружении `virtualenv` в локальной директории:

    ```bash
    python -m venv VENV

    # для ОС Linux:
    source VENV/bin/activate
    # для ОС Windows:
    VENV\Scripts\activate.bat

    pip install -r requirements.txt

    python main.py
    # Выход по Ctrl+C

    # Выход из виртуального окружения
    # для ОС Linux:
    deactivate
    # для ОС Windows:
    VENV\Scripts\deactivate.bat
    ```

6. Модуль тестирования `api_client.py` запускается вручную в той же виртуальной
среде, но в отдельной консоли. Для проверки логина с выдачей токена и для
проверки выдачи базы абонентов надо раскомментировать соответствующие строки в
разделе `MAIN`.

[:arrow_up: Содержание](#содержание)

----

## Мысли про SIP ##

:warning: Решить задачу работы с SIP-шлюзом &laquo;в лоб&raquo; не удалось.

В первую очередь возникает подозрение, что причина в имеющемся интернет-шлюзе,
который не обеспечивает нужную поддержку SIP ALG при трансляции адресов (NAT).
Для чистоты эксперимента предполагается организовать стенд, где проект будет
работать на хосте с &laquo;белым&raquo; IP-адресом (то есть напрямую смотрит в
интернет без NAT). Возможность есть, но нужно дополнительное время (отдельная
тестовая задачка :wink:).

Далее рассматриваются некоторые кандидаты на удачную отработку:
[**pyVoIP**](https://pyvoip.readthedocs.io/en/v1.6.5/#),
[**P2P-SIP**](https://github.com/theintencity/p2p-sip) (что сомнительно).

Наиболее перспективным на первый взгляд кажется
[**Most Voip Library**](https://most-voip.readthedocs.io/en/latest/index.html),
предварительно (и рекурсивно) требующая сборки и установки не-Python пакетов
[**PJSIP**](https://docs.pjsip.org/en/latest/index.html)
([**PJSIP на GIT**](https://github.com/pjsip/pjproject)),
[**PJSUA2**](https://docs.pjsip.org/en/latest/pjsua2/intro.html). Хотя он
предназначен в основном для работы с Asterisk, но мало ли.


[:arrow_up: Содержание](#содержание)

----
