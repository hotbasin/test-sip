#!/usr/bin/python3

from bottle import HTTPError, get, post, request, run

import api_srv as api_


''' =====----- Global variables -----===== '''

# Корневой index.html
ROOT_INDEX_FILE = 'adds_main/index.html'


''' =====----- Server resources -----===== '''

@get('/')
def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы Bottle
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    with open(ROOT_INDEX_FILE, 'r', encoding='utf-8') as f_:
        return f_.read()


@post('/srv1/auth/login')
def login_post() -> dict:
    ''' Ресурс аутентификации на сервере через метод POST
    '''
    return api_.login_getpost(request.json)


@post('/srv1/auth/login')
def login_get() -> dict:
    ''' Ресурс аутентификации на сервере через метод GET
    '''
    return api_.login_getpost(dict(request.query))


@post('/srv1/admin/adduser')
def adduser_post() -> dict:
    ''' Ресурс для добавления нового пользователя в базу
    '''
    return api_.adduser_post(**request.json)


@get('/srv1/abon/all')
def all_abon_get() -> dict:
    ''' Ресурс выдачи всей базы абонентов
    '''
    return api_.all_abon_get(req_data=request.query.req_data)


@post('/srv1/call/sample')
def call_sample_post():
    ''' Ресурс тестового звонка
    '''
    return api_.call_sample_post(**request.json)


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)

#####=====----- THE END -----=====#########################################