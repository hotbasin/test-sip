#!/usr/bin/python3

import json
from time import time, ctime

import requests
import jwt

TOKEN_FILE = 'acc-token.json'

def test_login(credentials: dict) -> str:
    ''' Тест аутентификации на ресурсе сервера.
    При удачном логине записывает полученный access-токен и его время
    окончания действия во временный файл, указанный в глобальной
    переменной TOKEN_FILE для использования в других тестах.
    Arguments:
        credentials [dict] -- Логин и пароль
    Returns:
        [str] -- Отформатированный многострочник со значениями
            text/acc_token/expired в случае успеха
            или со значением 'text' при ошибке
    '''
    r = requests.post('http://localhost:8080/srv1/auth/login', json=credentials)
    res_dict = r.json()
    if res_dict['status'] == 'success':
        text_ = res_dict['text']
        acc_token_ = res_dict['acc_token']
        expired_ = res_dict['expired']
        token_dict = {'acc_token': acc_token_,
                      'expired': expired_
                     }
        with open(TOKEN_FILE, 'w', encoding='utf-8') as j_:
            json.dump(token_dict, j_, ensure_ascii=False, indent=4)
        return f'Result: {text_}\nToken: {acc_token_}\nExpired: {ctime(expired_)}'
    else:
        return f'FAIL: {res_dict["text"]}'

''' =====----- MAIN -----===== '''
if __name__ == '__main__':
    # Раскомментировать для проверки логина
    creds = {'login': 'user1', 'password': 'qwerty1'}
    print(test_login(creds))

#####=====----- THE END -----=====#########################################