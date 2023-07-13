#!/usr/bin/python3

import json
import uuid

from bottle import HTTPError, get, post, request, run
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Session


''' =====----- Global variables -----===== '''

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
def login_post(credentials_: dict) -> dict:
    ''' Ресурс аутентификации на сервере
    Arguments:
        credentials_ [dict] -- Словарь/json с ключами 'login',
            'password'
    Returns:
        [dict] -- Словарь/json с токеном пользователя 'token',
            или с ключами 'code' и 'text' в случае ошибки    '''
    pass


''' =====----- MAIN -----===== '''
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)

#####=====----- THE END -----=====#########################################