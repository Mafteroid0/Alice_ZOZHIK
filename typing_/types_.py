from __future__ import annotations

import collections
import random
import typing
from collections import UserDict
import json
from typing import Dict, List


class KeyToAttrMixin(UserDict):
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


class FriendlyDict(KeyToAttrMixin):
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


class TrainingStep:
    def __init__(self, text: str, image: str,
                 title: str, description: str,
                 audio: str, detailed_description: str,
                 prev: TrainingStep | None = None, next_: TrainingStep | None = None):
        self.text = text
        self.image = image
        self.title = title
        self.description = description
        self.audio = audio
        self.detailed_description = detailed_description

        self.left = prev
        self.right = next_

    # def __repr__(self):
    # return f'{self.__class__.__name__}(req={self.data}, ' + (f', prev={self.left}' if self.left != self else '') + \
    #     (f', next={self.right}' if self.right != self else '') + ')'

    def __eq__(self, other: TrainingStep | None):
        return other is not None and \
            (self.text == other.text and
             self.description == other.description and
             self.audio == other.audio and
             self.left == other.left and
             self.right == other.right)

    def generate_choice_resp(self) -> dict[str, dict[
        str, dict[str, str] | str | list[dict[str, str | bool] | dict[str, str | bool] | dict[str, str | bool]]]]:
        return {
            'response': {
                'text': self.text,
                'card': {
                    'type': 'BigImage',
                    "image_id": self.image,
                    "title": self.title,
                    "description": self.description
                },
                'buttons': [
                    {
                        'title': 'Выполнить🔥',
                        'hide': True
                    },
                    {
                        'title': 'подробнее📄',
                        'hide': True
                    },
                    {
                        'title': 'Пропустить⏭',
                        'hide': True
                    }
                ]

            }
        }

    def generate_detailed_description_resp(self) -> dict[
        str, dict[str, str | list[dict[str, str | bool] | dict[str, str | bool]]]]:
        return {
            'response': {
                'text': self.detailed_description,
                'buttons': [
                    {
                        'title': 'Выполнить🔥',
                        'hide': True
                    },
                    {
                        'title': 'Пропустить⏭',
                        'hide': True
                    }
                ]

            }
        }

    def generate_do_training_resp(self, motivation: str) -> dict:
        return {
            'response': {
                'text': f'{motivation}',
                # TODO: 'tts': self.audio,
                'buttons': [
                    {
                        'title': 'Следующее упражнение▶',
                        'hide': True
                    }
                ]
            }
        }


class TrainingAlgorithm:
    def __init__(self, left: TrainingStep | None = None, right: TrainingStep | None = None):
        self.left = left

        self.right = left
        if right is None and left is not None:
            while self.right.right is not None:
                self.right = self.right.right

    def append_left(self, node: TrainingStep):
        node.right = self.left
        try:
            self.left.left = node
        except AttributeError:
            pass
        self.left = node

        if self.right is None:
            item = self.left
            for item in self:
                pass
            self.right = item

    def append_right(self, node: TrainingStep):
        node.left = self.right
        try:
            self.right.right = node
        except AttributeError:
            pass
        self.right = node

        if self.left is None:
            item = self.right
            for item in self:
                pass
            self.left = item

    append = append_right

    def __getitem__(self, item: int):
        a = 0
        node = self.left
        for node in self:
            if a >= item:
                break
            a += 1
        else:
            raise IndexError()
        return node

    def __repr__(self):
        node = self.left
        nodes = ['None']
        while node is not None:
            nodes.append(f'{node.data}')
            node = node.right
        if len(nodes) > 1:
            nodes.append('None')
        return ' <--> '.join(nodes)

    def __iter__(self):
        node = self.left
        if node is None:
            return StopIteration
        while node.right is not None:
            yield node
            node = node.right
        yield node

    def __reversed__(self):
        node = self.right
        while node.left is not None:
            yield node
            node = node.left
        yield node
