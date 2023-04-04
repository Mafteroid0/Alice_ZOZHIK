import typing
import random

from typing_ import ResponseField, Response, Item, Card, CardType
from fsm import FSMContext
from states import MainGroup


def show_main_menu(context: FSMContext, resp: dict | Response, text: str | typing.Sequence[str] | None = None,
                   card_text: str | None = None) -> dict | Response:
    answer_options = ['Приступаем к работе. Выбирайте чем займёмся:', 'Чем хотите заняться? Выбирайте:',
                      'Чем займёмся на этот раз? Выбирайте:',
                      'Вы уже в нескольких шагах от здорового образа жизни! Чем сегодня займёмся? Выбирайте:']
    resp.response = ResponseField(
        text='Это сообщение никто не увидит :(',
        tts=text or f'{random.choice(answer_options)} '
                    f'"Спортивные тренировки", "Водный баланс", "Идеальный вес", '
                    f'или "Фазы сна".',
        card=Card(
            type=CardType.ItemsList,
            header=card_text or ['Чем хотите заняться? Выбирайте:',

                                 'Приступаем к работе. Выбирайте чем займёмся:',

                                 'Чем займёмся на этот раз? Выбирайте:'
                                 ],
            items=[
                Item(
                    title='спортивные тренировки',
                    button='спортивные тренировки',
                    description='разнообразные комплексные тренировки',
                    image_id='965417/164c019491e4f4839bfa'
                ),
                Item(
                    title='водный баланс',
                    button='водный баланс',
                    description='расчёт дневной нормы воды',
                    image_id='1540737/dc7c3c075dd3ecc22fc7'
                ),
                Item(
                    title='фазы сна',
                    button='фазы сна',
                    description='Расчет идеального времени сна',
                    image_id='213044/e81c096eeedd03ef9a2e'
                ),
                Item(
                    title='идеальный вес',
                    button='идеальный вес',
                    description='расчёт индивидуальной нормы веса',
                    image_id='1540737/223b47fade7f44cbedfb'
                )
            ]
        )
    )
    MainGroup.main_menu.set(context)
    return resp