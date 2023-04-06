from flask import Flask, request

from typing_ import AliceUserRequest, RespDataClass, Response, ResponseField
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


def dict_to_json(dict_: dict | Response, *args, **kwargs):
    dict_ = trans_to_dict(dict_)
    return dict_


@application.route('/alice', methods=['POST'])
def handler():
    req = AliceUserRequest(request.data.decode())
    if req.request.original_utterance == 'ping' and req.request.command == '' and \
            req.request.type == 'SimpleUtterance':
        resp = Response(None, None, ResponseField(text='Ya work'))
    else:
        resp = main_handler(req, fsm)

    return dict_to_json(resp, ensure_ascii=False, indent=2)


def main():
    application.run('0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
