from __future__ import annotations

import copy
import random
import typing
from dataclasses import dataclass, field
from enum import Enum

from logging_ import logger, DO_LOGGING
from .request import Session


class _DefaultClass:
    pass


_DEFAULT = _DefaultClass

ButtonDict = dict[str, str | bool]

ItemButtonDict = dict[str, str]
ItemDict = dict[str, str | ItemButtonDict]

CardItemsListHeaderDict = dict[str, str]
CardDict = dict[str, str | CardItemsListHeaderDict | list[ItemDict] | list[ButtonDict]]

ResponseFieldDict = dict[str, str | CardDict]

ResponseDict = dict[str, str, ResponseFieldDict]

dict_models = (
    ButtonDict,
    ItemButtonDict,
    ItemDict,
    CardItemsListHeaderDict,
    CardDict,
    ResponseFieldDict,
    ResponseDict
)

DictPairModifier = typing.Callable[[str, typing.Any, typing.Callable | None], tuple[str, typing.Any]]


@dataclass
class RespDataClass:
    def to_dict(
            self,
            modifier: DictPairModifier | None = None,
            recursive: bool = True
    ) -> dict:
        modifier = modifier or self._modifier
        res = {}
        for annot_key in self.__annotations__.keys():
            key, value = annot_key, getattr(self, annot_key)

            if value is None:
                continue

            key, value = modifier(key, value, None)

            if hasattr(value, 'to_dict'):
                if recursive:
                    value = value.to_dict()
            elif isinstance(value, typing.Sequence) and not isinstance(value, str):
                value = [i.to_dict() if hasattr(i, 'to_dict') else i for i in value]

            res[key] = value

        if DO_LOGGING:
            logger.info(f'{self} transformated to {res}')

        return res

        # res = {}
        # for key in self.__annotations__.keys():
        #     value = getattr(self, key)
        #     if value is not None:
        #         res[key] = value
        # return res

    def _modifier(self, key: str, value: typing.Any, modifier: DictPairModifier | None = None):
        if key in ('text', 'tts') and isinstance(value, typing.Sequence) and not isinstance(value, str):
            value = random.choice(value)
        if modifier is not None:
            key, value = modifier(key, value, None)
        return key, value

    def update(self, udict: dict | RespDataClass, recursive: bool = False):
        for key, value in udict.items():

            if hasattr(value, 'update'):

                if recursive:

                    try:
                        value = getattr(self, key, value).update(value, recursive)
                    except TypeError:
                        value = getattr(self, key, value).update(value)

            setattr(self, key, value)

        return self

    def __getitem__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            try:
                return self.to_dict()[item]
            except KeyError:
                raise KeyError(f'{self} has not attribute {item}')

    def __setitem__(self, key, value):
        try:
            return self.__setattr__(key, value)
        except AttributeError:
            raise KeyError()

    def items(self):
        yield from ((key, value) for key, value in self.to_dict().items())

    def get(self, item, default: typing.Any | _DefaultClass = _DEFAULT):
        try:
            return self.__getitem__(item)
        except KeyError as e:
            if default is not _DEFAULT:
                return default
            else:
                raise e


@dataclass
class Button(RespDataClass):
    title: str
    hide: bool = True


@dataclass
class ItemButton(RespDataClass):
    text: str | typing.Sequence[str]


@dataclass
class Item(RespDataClass):
    title: str
    image_id: str
    button: str | ItemButton | ItemButtonDict | None = None
    description: str | None = None

    def _modifier(self, key: str, value: str | ItemButton | ItemButtonDict | None,
                  modifier: DictPairModifier | None = None):
        if key == 'button' and value == self.button and isinstance(value, str):
            value = {'text': value}
        return super()._modifier(key, value, modifier)


class CardType(Enum):
    ItemsList: str = 'ItemsList'
    BigImage: str = 'BigImage'

    def __repr__(self):
        return f'{self.name}'.split('.')[-1]

    __str__ = __repr__

    def to_dict(self) -> str:
        return f'{self}'


@dataclass
class AbstractCard(RespDataClass):
    type: CardType


@dataclass
class CardItemsListHeader(RespDataClass):
    text: str | typing.Sequence[str]


@dataclass
class ItemsListCard(AbstractCard, RespDataClass):
    type: CardType.ItemsList
    header: str | CardItemsListHeader | CardItemsListHeaderDict
    items: list[Item | ItemDict]

    def _modifier(self, key: str, value: str | ItemButton | ItemButtonDict | None,
                  modifier: DictPairModifier | None = None):
        if key == 'header' and value == self.header:
            if isinstance(value, str):
                value = {'text': value}
            elif isinstance(value, typing.Sequence):
                value = {'text': random.choice(value)}
        return super()._modifier(key, value, modifier)


@dataclass
class BigImageCard(AbstractCard, RespDataClass):
    type: CardType.BigImage
    image_id: str
    title: str
    description: str


@dataclass(kw_only=True)
class Card(ItemsListCard, BigImageCard):
    # Да, немного хардкод. Да, риск на несоответствие версий объектов.
    # Но как сделать лучше и чтобы при этом пайчарм видел тайпхинты я не придумал (посмотри на мой ник, лол)
    type: CardType
    header: str | typing.Sequence[str] | CardItemsListHeader | CardItemsListHeaderDict | None = None
    items: list[Item | ItemDict] | None = None
    image_id: str | None = None
    title: str | None = None
    description: str | None = None


@dataclass
class ResponseField(RespDataClass):
    text: str | typing.Sequence[str]
    tts: str | None = None
    card: Card | ItemsListCard | BigImageCard | CardDict | None = None
    buttons: list[Button | ButtonDict] = field(default_factory=lambda: copy.deepcopy([Button('Помощь', hide=False)]))


@dataclass
class Response(RespDataClass):
    version: str | None
    session: Session | None  # TODO: | SessionDict
    response: ResponseField | ResponseFieldDict | None = None


# r = Response(
#     version='1.0',
#     session='',
#     response=ResponseField(
#         text='Начинаем первое упражнение! Поочерёдное сгибание ног с последующим подниманием коленей к груди',
#         card=Card(
#             type=CardType.ItemsList,
#             header='Комментарий: Если на этот этап мы перешли с разминки, то об этом будет написано Приступаем к выполнению силовой тренировки.',
#             items=[
#                 Item(title='Я готов', button='Я готов', image_id='997614/72ab6692a3db3f4e3056'),
#                 Item(title='Выберем другую тренировку', button='Выберем другую тренировку',
#                      image_id='1030494/cc3631c8499cdc8daf8b')
#             ]
#         ),
#     )
# )
#
# print(r.response.card.to_dict())

__all__ = tuple(
    map(
        lambda cls: cls.__name__ if not isinstance(cls, str) else cls,
        (
            Response,
            ResponseField,
            Card,
            BigImageCard,
            ItemsListCard,
            Item,
            ItemButton,
            CardType,
            CardItemsListHeader,
            Button,
            Session,
            # SessionDict,
            'ButtonDict',
            'ItemButtonDict',
            'ItemDict',
            'CardItemsListHeaderDict',
            'CardDict',
            'ResponseFieldDict',
            'ResponseDict'
        )
    )
)
