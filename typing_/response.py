import copy
from dataclasses import dataclass, field, asdict
from enum import Enum

ButtonDict = dict[str, str | bool]

ItemButtonDict = dict[str, str]
ItemDict = dict[str, str | ItemButtonDict]

CardItemsListHeaderDict = dict[str, str]
CardDict = dict[str, str | CardItemsListHeaderDict | list[ItemDict] | list[ButtonDict]]

ResponseFieldDict = dict[str, str | CardDict]

ResponseDict = dict[str, str, ResponseFieldDict]


@dataclass
class RespDataClass:
    def to_dict(self) -> dict:
        return {key: value for key, value in asdict(self).items() if value is not None}

        # res = {}
        # for key in self.__annotations__.keys():
        #     value = getattr(self, key)
        #     if value is not None:
        #         res[key] = value
        # return res


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
    button: ItemButton | ItemButtonDict | None = None


class CardType(Enum):
    ItemsList: str = 'ItemsList'
    BigImage: str = 'BigImage'


@dataclass
class AbstractCard(RespDataClass):
    type: CardType


@dataclass
class CardItemsListHeader(RespDataClass):
    text: str


@dataclass
class ItemsListCard(AbstractCard, RespDataClass):
    type: CardType.ItemsList
    header: CardItemsListHeader
    items: list[Item | ItemDict]


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
    header: CardItemsListHeader | CardItemsListHeaderDict | None = None
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
            type=CardType.BigImage,
            image_id='997614/15bfafd8b629b323890b',
            title='Упражнение 1',
            description='Поочерёдное сгибание ног с последующим подниманием коленей к груди'
        ),
        buttons=[
            Button(title='Выполнить🔥'),
            Button(title='подробнее📄'),
            Button(title='Пропустить⏭')
        ]

    )
)

print(r.to_dict())
