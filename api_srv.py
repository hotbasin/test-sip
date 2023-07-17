#!/usr/bin/python3

import json
import uuid
from time import time

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Session
import jwt


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


''' =====----- Decorators -----===== '''

def auth_decor(fn_to_be_decor):
    ''' Декоратор для функций, которые в именованном аргументе 'req_data'
    получают данные в виде JSON Web Token.
    Распаковывает JWT, проверяет по базе наличие действительного
    access-tokena, по результату передаёт декорируемой функции
    именованный аргумент 'auth_ok' [bool] и полезную нагрузку в
    именованном аргументе 'payload'.
    '''
    def fn_wrapper(**kwargs):
        ok_ = False
        payload_ = dict()
        if 'req_data' in kwargs.keys():
            decoded_jwt_ = jwt.api_jwt.decode_complete(kwargs['req_data'],
                                                       key=JWT_KEY,
                                                       algorithms='HS256')
            header_ = decoded_jwt_['header']
            token_ = header_['acc_token']
            payload_ = decoded_jwt_['payload']
            try:
                with Session(ENGINE) as s_:
                    user_ = s_.query(User).filter(User.acc_token == token_).first()
                try:
                    if user_.expired > time():
                        # Время действия токена не закончилось
                        ok_ = True
                except:
                    # Токен закончился или его вообще нет
                    ok_ = False
            except:
                # Что-то не так с БД
                ok_ = False
        # Декорируемая функция
        result_ = fn_to_be_decor(auth_ok=ok_, payload=payload_, **kwargs)
        return result_
    return fn_wrapper


''' =====----- API Methods -----===== '''

def login_post(credentials: dict) -> dict:
    ''' Метод для ресурса аутентификации на сервере. В случае логина
    пользователя записывает для него в таблицу 'Users' выданный токен
    (token) и дату окончания его действия (expired).
    Arguments:
        credentials [dict] -- Словарь/json с ключами 'login', 'password'
    Returns:
        [dict] -- Словарь/json с ключами 'status', 'text', 'acc_token',
            'expired' или с ключами 'status', 'text' в случае ошибки.
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


@auth_decor
def adduser_post(auth_ok=False, payload=None, **kwargs) -> dict:
    ''' Метод для добавления нового пользователя в базу
    Arguments:
        auth_ok [bool] -- Запрос аутентифицирован
        payload [dict] -- Распакованная из JWT полезная нагрузка
            (словарь/json)
    Returns:
        [dict] -- Словарь/json с ключами status/...
    '''
    output_dict_ = {'status': 'fail',
                    'text': 'Unknown request'
                   }
    if auth_ok:
        new_user = User(uid=str(uuid.uuid4()),
                        name=payload['name'],
                        login=payload['login'],
                        password=payload['password'],
                        acc_token=None,
                        expired=None,
                        comment=payload['comment']
                       )
        try:
            with Session(ENGINE) as s_:
                if s_.query(User).filter(User.login == new_user.login).first():
                    output_dict_['text'] = 'User exists!'
                else:
                    s_.add(new_user)
                    s_.commit()
                    output_dict_['status'] = 'success'
                    output_dict_['text'] = f'User {new_user.login} added'
        except:
            # Ошибки работы с БД
            output_dict_['text'] = 'DS access error'
    else:
        # Токен закончился, надо обновить (снова залогиниться)
        output_dict_['text'] = 'Login required'

    return json.dumps(output_dict_, ensure_ascii=False, indent=2)


@auth_decor
def all_abon_get(auth_ok=False, payload=None, **kwargs):
    ''' Метод для выдачи всей базы абонентов
    Keyword Arguments:
        auth_ok [bool] -- Запрос аутентифицирован
        payload [dict] -- Распакованная из JWT полезная нагрузка
            (словарь/json)
    Returns:
        [dict] -- Словарь/json с ключами status/text/all_abon
            или с ключами status/text в случае ошибки
    '''
    output_dict_ = {'status': 'fail',
                    'text': 'Unknown request'
                   }
    if auth_ok:
        try:
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
        except:
            # Ошибки работы с БД
            output_dict_['text'] = 'DS access error'
    else:
        # Токен закончился, надо обновить (снова залогиниться)
        output_dict_['text'] = 'Login required'

    return json.dumps(output_dict_, ensure_ascii=False, indent=2)


@auth_decor
def call_sample_post(req_data=None, auth_ok=False, payload=None, **kwargs):
    ''' Метод для тестового звонка
    '''
    pass

#####=====----- THE END -----=====#########################################