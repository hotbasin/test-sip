#!/usr/bin/python3

import json
from time import ctime

import requests
import jwt


''' =====----- Global variables -----===== '''

# Временный файл для хранения access-токена
TOKEN_FILE = 'acc-token.json'
# Ключ для создания JSON Web Token
JWT_KEY = 'secretstring'


''' =====----- Functions -----===== '''

def test_login(credentials: dict) -> str:
    ''' Тест аутентификации на ресурсе сервера.
    Делает POST-запрос на сервер, login и password вкладывает в json.
    При удачном ответе в json {status: "success"} записывает полученный
    access-токен и его время окончания действия (в читаемом формате) во
    временный файл, указанный в глобальной переменной TOKEN_FILE для
    использования в других тестах.
    Arguments:
        credentials [dict] -- Логин и пароль
    Returns:
        [str] -- Отформатированный многострочник со значениями
            text/acc_token/expired в случае успеха
            или со значением 'text' при ошибке
    '''
    r_ = requests.post('http://localhost:8080/srv1/auth/login',
                       json=credentials)
    res_dict = r_.json()
    if res_dict['status'] == 'success':
        text_ = res_dict['text']
        acc_token_ = res_dict['acc_token']
        expired_ = res_dict['expired']
        token_dict = {'acc_token': acc_token_,
                      'expired': ctime(expired_)
                     }
        with open(TOKEN_FILE, 'w', encoding='utf-8') as j_:
            json.dump(token_dict, j_, ensure_ascii=False, indent=4)
        return f'Result: {text_}\nToken: {acc_token_}\nExpired: {ctime(expired_)}'
    else:
        return f'FAIL: {res_dict["text"]}'


def test_adduser(adduserdata: dict) -> str:
    ''' Тест добавления нового пользователя в базу
    Arguments:
        adduserdata [dict] -- Данные нового пользователя с ключами
            'name', 'login', 'password', 'comment'
    Returns:
        [str] -- Неотформатированный многострочник с полученным от
            сервера json-ответом
    '''
    with open(TOKEN_FILE, 'r', encoding='utf-8') as j_:
        token_dict_ = json.load(j_)
    acc_token_ = token_dict_['acc_token']
    req_jwt_ = jwt.encode(adduserdata, JWT_KEY, algorithm='HS256',
                          headers={'acc_token': acc_token_}
                         )
    r_ = requests.post('http://localhost:8080/srv1/admin/adduser',
                       json={'req_data': req_jwt_})
    return r_.text


def test_abon() -> str:
    ''' Тест выдачи всей базы абонентов.
    Отправляет в GET-запросе на сервер закодированный JSON Web Token.
    В 'header' добавляет полученный при логине access-токен.
    В 'payload' в данном случае можно включить пустой словарь.
    Returns:
        [str] -- Неотформатированный многострочник с полученным от
            сервера json-ответом
    '''
    with open(TOKEN_FILE, 'r', encoding='utf-8') as j_:
        token_dict_ = json.load(j_)
    payload_ = {}
    acc_token_ = token_dict_['acc_token']
    req_jwt_ = jwt.encode(payload_, JWT_KEY, algorithm='HS256',
                          headers={'acc_token': acc_token_}
                         )
    r = requests.get('http://localhost:8080/srv1/abon/all',
                     params={'req_data': req_jwt_}
                    )
    return r.text


def test_call(phone_number: str) -> str:
    import client_confidentials as cc_
    call_attribs_ = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as j_:
        token_dict_ = json.load(j_)
    acc_token_ = token_dict_['acc_token']
    call_attribs_['gw_addr'] = cc_.SIP_GW_IP
    call_attribs_['gw_login'] = cc_.SIP_GW_ID
    call_attribs_['gw_password'] = cc_.SIP_GW_PW
    call_attribs_['phone_num'] = phone_number
    req_jwt_ = jwt.encode(call_attribs_, JWT_KEY, algorithm='HS256',
                          headers={'acc_token': acc_token_}
                         )
    r_ = requests.post('http://localhost:8080/srv1/call/sample',
                       json={'req_data': req_jwt_})
    return r_.text


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    ''' Раскомментировать для проверки логина и для повторной авторизации
    при окончании действия токена (POST)
    '''
    creds = {'login': 'user1', 'password': 'qwerty1'}
    print(test_login(creds))
    
    ''' Раскомментировать для проверки выдачи абонентской базы (GET)
    '''
    # print(test_abon())
    
    ''' Раскомментировать для проверки добавления пользователя в базу (POST)
    '''
    # new_user = {'name': 'Johan', 'login': 'user4', 'password': 'qwerty4', 'comment': ''}
    # print(test_adduser(new_user))
    
    ''' Раскомментировать для проверки тестового звонка
    '''
    phone_number = '80951234567'
    print(test_call(phone_number))

#####=====----- THE END -----=====#########################################