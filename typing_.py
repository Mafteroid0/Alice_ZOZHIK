from __future__ import annotations
import typing
from collections import UserDict
import json
import inspect


class FriendlyDict(UserDict):
    @staticmethod
    def _make_dict_available(d: dict[str, typing.Any],
                             annotations: dict[str, type],
                             aggressive: bool = True) -> dict[str, typing.Any]:
        for key, value in d.items():
            value_excepted_type = annotations[key]
            if type(value) != value_excepted_type:  # Потому что пайчарм ругается на isinstance
                if issubclass(value_excepted_type, FriendlyDict) and value_excepted_type != FriendlyDict:
                    d[key] = value_excepted_type(value)
                    continue
                if aggressive:
                    raise ValueError()
        return d

    def __init__(self, *args, aggressive: bool = True, **kwargs):
        if len(args) > 0:
            first_arg = args[0]
            if isinstance(first_arg, str):
                first_arg = json.loads(first_arg)
            kwargs.update(first_arg)

        kwargs = self._make_dict_available(kwargs,
                                           typing.get_type_hints(self.__class__),
                                           aggressive=aggressive)

        self.data = {}
        self.data.update(kwargs)

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError as e:
            try:
                return self.get(item)
            except KeyError:
                raise e

    # def __setattr__(self, key, value): # Maybe in future
    #     try:
    #         super().__setattr__(key, value)
    #     except AttributeError as e:
    #         try:
    #             self[key] = value
    #         except KeyError:
    #             raise e


class ExampleDict(FriendlyDict):
    id: int
    da: bool


class RequestMetaInterfaces(FriendlyDict):
    screen: dict
    account_linking: dict
    audio_player: dict


class RequestMeta(FriendlyDict):
    locale: str
    timezone: str
    client_id: str
    interfaces: RequestMetaInterfaces


req_meta = RequestMeta({
    "locale": "ru-RU",
    "timezone": "Europe/Moscow",
    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
    "interfaces": {
        "screen": {},
        "account_linking": {},
        "audio_player": {}
    }
})

print(req_meta)
print(req_meta.interfaces)
