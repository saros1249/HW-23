import os

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def do_cmd(cmd, value, data):
    """
    Обрабатывает запрос при помощи Query.
    :param cmd: команда query
    :param value: аргумент команды query
    :param data: list данные для обработки.
    :return: list
    """
    if cmd == 'filter':
        cmd_res = list(filter(lambda record: value in record, data))
    elif cmd == 'map':
        col_num = int(value)
        if col_num == 0:
            cmd_res = list(map(lambda record: record.split()[col_num], data))
        elif col_num == 1:
            cmd_res = list(map(lambda record: record.split()[3] + record.split()[4], data))
        elif col_num == 2:
            cmd_res = list(map(lambda record: ' '.join(record.split()[5:]), data))
        else:
            raise BadRequest
    elif cmd == 'unique':
        cmd_res = list(set(data))
    elif cmd == 'sort':
        reverse = (value == 'desc')
        cmd_res = sorted(data, reverse=reverse)
    elif cmd == 'limit':
        cmd_res = data[:int(value)]
    else:
        raise BadRequest
    return cmd_res


def do_query(param):
    """
    Обрабатывает запрос, получает json, возвращает результат в виде списка.
    :param json
    :return: list
    """
    with open(os.path.join(DATA_DIR, param['file_name'])) as f:
        file_data = f.readlines()

    res = file_data

    if 'cmd1' in param.keys():
        res = do_cmd(param['cmd1'], param['value1'], res)

    if 'cmd2' in param.keys():
        res = do_cmd(param['cmd2'], param['value2'], res)

    return res


@app.route("/perform_query", methods=['POST'])
def perform_query():
    req = request.json

    if not req:
        raise BadRequest

    if not os.path.exists(os.path.join(DATA_DIR, req['file_name'])):
        raise BadRequest

    return jsonify(do_query(req))


if __name__ == '__main__':
    app.run()
