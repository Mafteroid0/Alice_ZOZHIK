from __future__ import annotations
import dataclasses
import random
import typing


@dataclasses.dataclass
class TrainingStep:
    text: str | typing.Sequence[str]
    image: str | typing.Sequence[str]
    title: str | typing.Sequence[str]
    description: str | typing.Sequence[str]
    detailed_description: str | typing.Sequence[str]

    left: TrainingStep | None = None
    right: TrainingStep | None = None

    def generate_choice_resp(self) -> dict[str, dict[
        str, dict[str, str] | str | list[dict[str, str | bool] | dict[str, str | bool] | dict[str, str | bool]]]]:
        return {
            'response': {
                'text': self.text if isinstance(self.text, str) else random.choice(self.text),
                'card': {
                    'type': 'BigImage',
                    "image_id": self.image if isinstance(self.image, str) else random.choice(self.image),
                    "title": self.title if isinstance(self.title, str) else random.choice(self.title),
                    "description": self.description if isinstance(self.description, str) else random.choice(
                        self.description)
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

    @staticmethod
    def generate_do_training_resp(motivation: str, track: str) -> dict:
        return {
            'response': {
                'text': f'{motivation}',
                'tts': f'{track}',
                'buttons': [
                    {
                        'title': 'Следующее упражнение▶',
                        'hide': True
                    }
                ]
            }
        }


class TrainingDialog:
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
            nodes.append(f'{node}')
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
