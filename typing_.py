from __future__ import annotations

import dis
import typing
from collections import UserDict
import json
import inspect


class FriendlyDict(UserDict):
    @staticmethod
    def _make_dict_available(d: dict[str, typing.Any],
                             annotations: dict[str, type],
                             aggressive: bool = False) -> dict[str, typing.Any]:
        for key, value in d.items():
            try:
                value_excepted_type = annotations[key]
            except KeyError:
                if aggressive:
                    raise TypeError(f'Dict item {key} not mentioned in the annotations')
                continue
            if type(value) != value_excepted_type:  # Потому что пайчарм ругается на isinstance
                if issubclass(value_excepted_type, FriendlyDict) and value_excepted_type != FriendlyDict:
                    d[key] = value_excepted_type(value)
                    continue
                if aggressive:
                    raise TypeError(f'Dict item {key} have type {type(value)}, but excepted {value_excepted_type}')
        return d

    def __init__(self, *args, aggressive: bool = False, **kwargs):
        if len(args) > 0:
            first_arg = args[0]
            if isinstance(first_arg, str):
                first_arg = json.loads(first_arg)
            try:
                kwargs.update(first_arg)
            except TypeError as e:
                print(first_arg)
                raise e

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

    def to_dict(self) -> dict:
        for key, value in self.data.items():
            try:
                json.dumps(value)
            except TypeError:
                self.data[key] = value.to_dict()
        return self.data


class ExampleDict(FriendlyDict):
    id: int
    da: bool


class RequestMetaInterfaces(FriendlyDict):
    screen: dict
    account_linking: dict
    audio_player: dict


class Meta(FriendlyDict):
    locale: str
    timezone: str
    client_id: str
    interfaces: RequestMetaInterfaces


class RequestField(FriendlyDict):
    type: str
    command: str


class User(FriendlyDict):
    user_id: str
    access_token: str


class Application(FriendlyDict):
    application_id: str


class Session(FriendlyDict):
    message_id: int
    session_id: str
    skill_id: str
    user_id: str
    user: User
    application: Application
    new: bool


class YaSessionState(FriendlyDict):
    value: int


class YaUserState(FriendlyDict):
    value: int


class YaApplicationState(FriendlyDict):
    value: int


class YaState(FriendlyDict):
    session: YaSessionState
    user: YaUserState
    application: YaApplicationState


class AliceUserRequest(FriendlyDict):
    meta: Meta
    request: RequestField
    session: Session
    state: YaState
    version: str


print(AliceUserRequest({
  "meta": {
    "locale": "ru-RU",
    "timezone": "Europe/Moscow",
    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
    "interfaces": {
      "screen": {},
      "account_linking": {},
      "audio_player": {}
    }
  },
  "request": {
    "type": "..."
  },
  "session": {
    "message_id": 0,
    "session_id": "2eac4854-fce721f3-b845abba-20d60",
    "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
    "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8",
    "user": {
      "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
      "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT"
    },
    "application": {
      "application_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8"
    },
    "new": True
  },
  "state": {
    "session": {
      "value": 10
    },
    "user": {
      "value": 42
    },
    "application": {
      "value": 37
    }
  },
  "version": "1.0"
}).to_dict())
