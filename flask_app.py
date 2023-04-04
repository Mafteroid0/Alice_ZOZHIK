from flask import Flask, request

from logging_ import logged
from typing_.response import RespDataClass, Response
from typing_ import AliceUserRequest
from fsm import FSMContext

from handlers import main_handler

application = Flask(__name__)

fsm = FSMContext()


def trans_to_dict(dict_: dict | RespDataClass) -> dict:
    if hasattr(dict_, 'to_dict'):
        dict_ = dict_.to_dict()
    else:
        for key, value in dict_.items():
            if hasattr(value, 'to_dict'):
                value = value.to_dict()
            dict_[key] = value
    return dict_


def encode(dict_: dict):
    for key, value in dict_.items():
        if isinstance(value, str):
            dict_[key] = value.encode()
    return dict_


def dict_to_json(dict_: dict | Response, do_encode: bool = True, *args, **kwargs):
    dict_ = trans_to_dict(dict_)
    return dict_


@application.route('/alice', methods=['POST'])
def handler():
    req = AliceUserRequest(request.data.decode())
    return dict_to_json(main_handler(req, fsm), ensure_ascii=False, indent=2)


def main():
    application.run('localhost', port=5050, debug=True)


if __name__ == '__main__':
    main()
