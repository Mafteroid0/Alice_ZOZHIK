import typing
from collections import UserDict
import json


class FriendlyDict(UserDict):
    @staticmethod
    def _dict_is_available(d: dict[str, typing.Any], annotations: dict[str, type]):
        for key, value in d.items():
            value_excepted_type = annotations[key]
            if type(value) != value_excepted_type:  # Потому что пайчарм ругается на isinstance
                return False
        return True

    def __init__(self, *args, aggressive: bool = True, **kwargs):
        if len(args) > 0 and isinstance(first_arg := args[0], str):
            kwargs.update(json.loads(first_arg))

        print(self._dict_is_available(kwargs, self.__class__.__dict__['__annotations__']))
        if aggressive and not self._dict_is_available(kwargs, self.__class__.__dict__['__annotations__']):
            raise ValueError()

        self.data = {}
        self.data.update(kwargs)

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError as e:
            try:
                return self[item]
            except KeyError:
                raise e


class ExampleDict(FriendlyDict):
    id: int
    da: bool

