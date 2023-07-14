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
def login_post():
    ''' Ресурс аутентификации на сервере
    '''
    return api_.login_post(request.json)

@get('/srv1/abon/all')
def abon_get():
    ''' Ресурс выдачи всей базы абонентов
    '''
    req_data_ = request.query.req_data
    return api_.abon_get(req_data_)

''' =====----- MAIN -----===== '''
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)

#####=====----- THE END -----=====#########################################