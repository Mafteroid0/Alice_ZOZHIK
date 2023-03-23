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
            try:
                kwargs.update(first_arg)
            except TypeError:
                print(first_arg)

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
