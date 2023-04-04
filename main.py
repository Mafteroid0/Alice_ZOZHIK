from typing_.response import RespDataClass, Response
from typing_ import AliceUserRequest
from fsm import FSMContext

from handlers import main_handler

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


def dict_to_json(dict_: dict | Response):
    dict_ = trans_to_dict(dict_)
    return dict_


def main(event, context):
    req = AliceUserRequest(event)
    return dict_to_json(main_handler(req, fsm))
