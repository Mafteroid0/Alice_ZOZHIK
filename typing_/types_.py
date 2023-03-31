from __future__ import annotations

import collections
import dataclasses
import random
import typing
from collections import UserDict
import json
from typing import Dict, List


class KeyToAttr(UserDict):
    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError as e:
            try:
                return super().get(item)
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


class FriendlyDict(KeyToAttr):
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

    def to_dict(self) -> dict:
        for key, value in self.data.items():
            try:
                json.dumps(value)
            except TypeError:
                self.data[key] = value.to_dict()
        return self.data
