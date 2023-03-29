from .request import *
from .types_ import FriendlyDict
from .dialogs import TrainingDialog, TrainingStep


def to_dict(dict_: dict) -> dict:
    for key, value in dict_.items():
        try:
            dict_[key] = value.to_dict()
        except AttributeError:
            pass
    return dict_
