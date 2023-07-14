#!/usr/bin/python3

import json
import uuid
from time import time

# from bottle import HTTPError, get, post, request, run
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Session


''' =====----- Global variables -----===== '''

# Настройки для SQLAlchemy
DB_PATH = 'sqlite:///sqlite/db.sqlite3'
Base = declarative_base()
ENGINE = sa.create_engine(DB_PATH)
# Время действия логина на сервер в секундах
LOGIN_INTERVAL = 600.0


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


def login_post(credentials: dict) -> dict:
    ''' Метод для ресурса аутентификации на сервере. В случае логина
    польщователя записывает для него в таблицу Users выданный токен
    (token) и дату окончания его действия (expired).
    Arguments:
        credentials [dict] -- Словарь/json с ключами 'login', 'password'
    Returns:
        [dict] -- Словарь/json с ключами status/text/token, или
            с ключами status/text в случае ошибки
    '''
    output_ = {'status': 'fail',
               'text': 'Unknown error'
              }
    try:
        with Session(ENGINE) as s_:
            login_ = credentials['login']
            password_ = credentials['password']
            user_ = s_.query(User).filter(User.login == login_).first()
            if user_:
                if user_.password == password_:
                    token_ = str(uuid.uuid4())
                    # Обновление пользователя в базе
                    user_.token = token_
                    user_.expired = time() + LOGIN_INTERVAL
                    s_.add(user_)
                    s_.commit()
                    # Возврат токена
                    output_['status'] = 'success'
                    output_['text'] = f'User {login_}: logged in'
                    output_['token'] = token_
                else:
                    output_['status'] = 'fail'
                    output_['text'] = f'User {login_}: login failed'
            else:
                output_['status'] = 'fail'
                output_['text'] = f'User {login_}: not exists'
    except:
        pass
    return json.dumps(output_, ensure_ascii=False)

#####=====----- THE END -----=====#########################################