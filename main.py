#!/usr/bin/python3

from bottle import HTTPError, get, post, request, run


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


''' =====----- MAIN -----===== '''
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)

#####=====----- THE END -----=====#########################################