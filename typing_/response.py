import copy
import json
import typing
from dataclasses import dataclass, field
from enum import Enum

ButtonDict = dict[str, str | bool]

ItemButtonDict = dict[str, str]
ItemDict = dict[str, str | ItemButtonDict]

CardItemsListHeaderDict = dict[str, str]
CardDict = dict[str, str | CardItemsListHeaderDict | list[ItemDict] | list[ButtonDict]]

ResponseFieldDict = dict[str, str | CardDict]

ResponseDict = dict[str, str, ResponseFieldDict]

DictPairModifier = typing.Callable[[str, typing.Any, typing.Callable | None], tuple[str, typing.Any]]


@dataclass
class RespDataClass:
    def to_dict(
            self,
            modifier: DictPairModifier | None = None
    ) -> dict:
        print()
        print(self)
        modifier = modifier or self._modifier
        res = {}
        for annot_key in self.__annotations__.keys():
            key, value = annot_key, getattr(self, annot_key)
            print(key, value)
            if value is None:
                continue

            key, value = modifier(key, value, None)

            if hasattr(value, 'to_dict'):
                value = value.to_dict()
            elif isinstance(value, typing.Sequence) and not isinstance(value, str):
                value = [i.to_dict() if hasattr(i, 'to_dict') else i for i in value]
                print('\t', value)

            res[key] = value
        return res

        # res = {}
        # for key in self.__annotations__.keys():
        #     value = getattr(self, key)
        #     if value is not None:
        #         res[key] = value
        # return res

    def _modifier(self, key: str, value: typing.Any, modifier: DictPairModifier | None = None):
        return (modifier or (lambda _key, _value, _: (_key, _value)))(key, value, None)


@dataclass
class Button(RespDataClass):
    title: str
    hide: bool = True


@dataclass
class ItemButton(RespDataClass):
    text: str


@dataclass
class Item(RespDataClass):
    title: str
    image_id: str
    button: str | ItemButton | ItemButtonDict | None = None

    def _modifier(self, key: str, value: str | ItemButton | ItemButtonDict | None,
                  modifier: DictPairModifier | None = None):
        if key == 'button' and value == self.button and isinstance(value, str):
            value = {'text': value}
        return (modifier or super()._modifier)(key, value, modifier)


class CardType(Enum):
    ItemsList: str = 'ItemsList'
    BigImage: str = 'BigImage'

    def __str__(self):
        return f'{self.name}'.split('.')[-1]

    def to_dict(self) -> str:
        return f'{self}'


@dataclass
class AbstractCard(RespDataClass):
    type: CardType


@dataclass
class CardItemsListHeader(RespDataClass):
    text: str


@dataclass
class ItemsListCard(AbstractCard, RespDataClass):
    type: CardType.ItemsList
    header: str | CardItemsListHeader | CardItemsListHeaderDict
    items: list[Item | ItemDict]

    def _modifier(self, key: str, value: str | ItemButton | ItemButtonDict | None,
                  modifier: DictPairModifier | None = None):
        if key == 'header' and value == self.header and isinstance(value, str):
            value = {'text': value}
        return (modifier or super()._modifier)(key, value, modifier)


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
    header: str | CardItemsListHeader | CardItemsListHeaderDict | None = None
    items: list[Item | ItemDict] | None = None
    image_id: str | None = None
    title: str | None = None
    description: str | None = None


@dataclass
class ResponseField(RespDataClass):
    text: str
    tts: str | None = None
    card: Card | ItemsListCard | BigImageCard | CardDict | None = None
    buttons: list[Button | ButtonDict] = field(default_factory=lambda: copy.deepcopy([Button('Помощь', hide=False)]))


@dataclass
class Response(RespDataClass):
    version: str
    session: str
    response: ResponseField | dict


r = Response(
    version='1.0',
    session='',
    response=ResponseField(
        text='Начинаем первое упражнение! Поочерёдное сгибание ног с последующим подниманием коленей к груди',
        card=Card(
            type=CardType.ItemsList,
            header='Комментарий: Если на этот этап мы перешли с разминки, то об этом будет написано Приступаем к выполнению силовой тренировки.',
            items=[
                Item(title='Я готов', button='Я готов', image_id='997614/72ab6692a3db3f4e3056'),
                Item(title='Выберем другую тренировку', button='Выберем другую тренировку',
                     image_id='1030494/cc3631c8499cdc8daf8b')
            ]
        ),
    )
)

print(json.dumps(r.to_dict()))

__all__ = tuple(
    map(
        lambda cls: cls.__name__,
        reversed(
            (
                Response,
                ResponseDict,
                ResponseField,
                ResponseFieldDict,
                Card,
                BigImageCard,
                ItemsListCard,
                Item,
                ItemDict,
                ItemButton,
                ItemButtonDict,
                CardDict,
                CardType,
                CardItemsListHeader,
                CardItemsListHeaderDict,
                Button,
                ButtonDict
            )
        )
    )
)
