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
# Ключ для создания JSON Web Token
JWT_KEY = 'secretstring'


''' =====----- Classes -----===== '''

class User(Base):
    __tablename__ = 'Users'
    uid = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(1024))
    login = sa.Column(sa.String(1024))
    password = sa.Column(sa.String(1024))
    acc_token = sa.Column(sa.String(1024))
    expired = sa.Column(sa.Float)
    comment = sa.Column(sa.Text(1024))

class Abon(Base):
    __tablename__ = 'Callbase'
    cid = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(1024))
    number = sa.Column(sa.String(12))
    comment = sa.Column(sa.Text(1024))


''' =====----- API Methods -----===== '''

def login_post(credentials: dict) -> dict:
    ''' Метод для ресурса аутентификации на сервере. В случае логина
    польщователя записывает для него в таблицу Users выданный токен
    (token) и дату окончания его действия (expired).
    Arguments:
        credentials [dict] -- Словарь/json с ключами 'login', 'password'
    Returns:
        [dict] -- Словарь/json с ключами status/text/acc_token/expired
            или с ключами status/text в случае ошибки
    '''
    output_dict_ = {'status': 'fail',
                    'text': 'Unknown request'
                   }
    try:
        with Session(ENGINE) as s_:
            login_ = credentials['login']
            password_ = credentials['password']
            user_ = s_.query(User).filter(User.login == login_).first()
            if user_:
                if user_.password == password_:
                    acc_token_ = str(uuid.uuid4())
                    # Обновление пользователя в базе
                    user_.acc_token = acc_token_
                    user_.expired = time() + LOGIN_INTERVAL
                    s_.add(user_)
                    s_.commit()
                    # Возврат токена
                    output_dict_['status'] = 'success'
                    output_dict_['text'] = f'User {login_}: logged in'
                    output_dict_['acc_token'] = acc_token_
                    output_dict_['expired'] = user_.expired
                else:
                    output_dict_['text'] = f'User {login_}: login failed'
            else:
                output_dict_['text'] = f'User {login_}: not exists'
    except:
        pass
    return json.dumps(output_dict_, ensure_ascii=False, indent=2)


def all_abon_get(req_data):
    ''' Метод для выдачи всей базы абонентов
    Arguments:
        req_data --
    Returns:
        [dict] -- Словарь/json с ключами status/text/all_abon
            или с ключами status/text в случае ошибки
    '''
    output_dict_ = {'status': 'fail',
                    'text': 'Unknown request'
                   }
    # try:
    with Session(ENGINE) as s_:
            abonents_ = s_.query(Abon).all()
    n_ = 0
    abon_dict_ = {}
    for abon_ in abonents_:
            n_ += 1
            abon_dict_[n_] = dict(name=abon_.name,
                                  number=abon_.number,
                                  comment=abon_.comment
                                 )
    output_dict_['status'] = 'success'
    output_dict_['text'] = 'Authorized request'
    output_dict_['all_abon'] = abon_dict_
    """except:
        output_dict_['text'] = 'DS access error'"""

    return json.dumps(output_dict_, ensure_ascii=False, indent=2)


def call_sample_post():
    ''' Метод для тестового звонка
    '''
    pass

#####=====----- THE END -----=====#########################################