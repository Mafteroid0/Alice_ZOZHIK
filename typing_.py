from __future__ import annotations
import typing
from collections import UserDict
import json
import inspect


class FriendlyDict(UserDict):
    def _make_dict_available(self, d: dict[str, typing.Any],
                             annotations: dict[str, type],
                             aggressive: bool = True) -> UserDict[str, typing.Any]:
        for key, value in d.items():
            value_excepted_type = annotations[key]
            if type(value).__name__ != value_excepted_type:  # Потому что пайчарм ругается на isinstance
                print([value_excepted_type])
                if i and issubclass(value_excepted_type, FriendlyDict):
                    d[key] = value_excepted_type(value)
                    continue
                if aggressive:
                    raise ValueError()
        return FriendlyDict(d) if not type(d) == type(self) else d

    def __init__(self, *args, aggressive: bool = True, **kwargs):
        if len(args) > 0:
            if isinstance(first_arg := args[0], str):
                first_arg = json.loads(first_arg)
            kwargs.update(first_arg)

        print(kwargs := self._make_dict_available(kwargs,
                                                  self.__class__.__annotations__,
                                                  aggressive=aggressive))

        self.data = {}
        self.data.update(kwargs)

    def __getattribute__(self, item):
        try:
            # print(super())
            return super().__getattribute__(item)
        except AttributeError as e:
            try:
                return self.get(item)
            except KeyError:
                raise e


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
print(req_meta.interfaces.audio_player)
