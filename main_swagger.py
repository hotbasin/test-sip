#!/usr/bin/python3

import os
cur_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(cur_dir, 'swagger_conf/swagger.yaml')

from bottle import Bottle, HTTPError, request, run
from swagger_ui import bottle_api_doc

import api_srv as api_


''' =====----- Global variables -----===== '''

app = Bottle()
# Корневой index.html
ROOT_INDEX_FILE = 'adds_main/index.html'


''' =====----- Server resources -----===== '''

@app.route('/', method='GET')
def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы Bottle
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    with open(ROOT_INDEX_FILE, 'r', encoding='utf-8') as f_:
        return f_.read()


@app.route('/srv1/auth/login', method='POST')
def login_post() -> dict:
    ''' Ресурс аутентификации на сервере через метод POST
    '''
    return api_.login_getpost(request.json)


@app.route('/srv1/auth/login', method='GET')
def login_get() -> dict:
    ''' Ресурс аутентификации на сервере через метод GET
    '''
    return api_.login_getpost(dict(request.query))


@app.route('/srv1/admin/adduser', method='POST')
def adduser_post() -> dict:
    ''' Ресурс для добавления нового пользователя в базу
    '''
    return api_.adduser_post(**request.json)


@app.route('/srv1/abon/all', method='GET')
def all_abon_get() -> dict:
    ''' Ресурс выдачи всей базы абонентов
    '''
    return api_.all_abon_get(req_data=request.query.req_data)


@app.route('/srv1/call/sample', method='POST')
def call_sample_post():
    ''' Ресурс тестового звонка
    '''
    return api_.call_sample_post(**request.json)


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    bottle_api_doc(app, config_path=config_path, url_prefix='/api/doc', title='Swagger docs')
    run(app, host='0.0.0.0', port=8080, debug=True)

#####=====----- THE END -----=====#########################################