#!/usr/bin/python3

import json
import uuid
from time import time

from bottle import HTTPError, get, post, request, run
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Session

##### import srv_api as api_


''' =====----- Global variables -----===== '''

ROOT_INDEX_FILE = 'adds_main/index.html'
# Настройки для SQLAlchemy
DB_PATH = 'sqlite:///sqlite/db.sqlite3'
Base = declarative_base()
ENGINE = sa.create_engine(DB_PATH)
# Время действия логина на сервер в секундах
LOGIN_INTERVAL = 3600.0


''' =====----- Classes -----===== '''

class User(Base):
    __tablename__ = 'Users'
    uid = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(1024))
    login = sa.Column(sa.String(1024))
    password = sa.Column(sa.String(1024))
    token = sa.Column(sa.String(1024))
    expired = sa.Column(sa.Float)
    comment = sa.Column(sa.Text(1024))


class Abon(Base):
    __tablename__ = 'Callbase'
    cid = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(1024))
    number = sa.Column(sa.String(12))


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
# def login_post(credentials_: dict) -> dict:
def login_post(login_: str, password_: str) -> object:
    ''' Ресурс аутентификации на сервере
    Arguments:
        credentials_ [dict] -- Словарь/json с ключами 'login',
            'password'
    Returns:
        [dict] -- Словарь/json с токеном пользователя 'token',
            или с ключами 'code' и 'text' в случае ошибки    '''
    with Session(ENGINE) as s_:
        try:
            user_ = s_.query(User).filter(User.login == login_).first()
            if user_.password == password_:
                token_ = str(uuid.uuid4())
                output_ = dict(status='success',
                               token=token_
                              )
                user_.token = token_
                user_.expired = time() + 600.0
                s_.add(user_)
                s_.commit()
            else:
                output_ = dict(status='fail',
                               text='Login failed'
                              )
        except:
            output_ = dict(status='fail',
                           text='Authentication error'
                          )
    return json.dumps(output_, ensure_ascii=False)


''' =====----- MAIN -----===== '''
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)

#####=====----- THE END -----=====#########################################