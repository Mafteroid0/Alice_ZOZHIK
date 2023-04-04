import random

from typing_ import Response, AliceUserRequest, ResponseField, Card, CardType, Item
from fsm import FSMContext

from states import MainGroup


def water_handler(context: FSMContext, req: AliceUserRequest, resp: dict | Response) -> dict | Response:
    state = context.state
    command = req.request.command

    if state == MainGroup.Water.state_1:
        st = command.replace(',', '.')
        li = st.split(' ')
        for el in li:
            el = el.replace(',', '.')
            if el.replace('.', '').isdecimal() and el.count('.') <= 1:
                water_amount = int(float(el) * 30)
                answer_options = [
                    f'Ваше минимальное потребление воды {water_amount} миллилитров в день 💦',

                    f'Вам необходимо {water_amount} миллилитров воды 🌊 в день, для хорошего метаболизма.']

                resp.response = ResponseField(
                    text=answer_options,
                    card=Card(
                        type=CardType.ItemsList,
                        header=answer_options,
                        items=[
                            Item(
                                title='Рассчитать ещё раз',
                                button='Рассчитать ещё раз',
                                description='',
                                image_id='997614/15f977696a281092bcc0'
                            ),
                            Item(
                                title='Вернуться к основному списку',
                                button='Назад',
                                description='',
                                image_id='1030494/cc3631c8499cdc8daf8b'
                            )
                        ]
                    )
                )

                context.set_state(MainGroup.Water.end)
                break
            else:
                resp.update({
                    'response': {
                        'text': f'Не совсем поняла вас. Назовите ваш вес в килограммах.'
                    }
                })
    elif state == MainGroup.Water.end and \
            ('ещё' in command or 'счит' in command):
        resp.response = ResponseField(
            text=[
                'Подскажите Ваш вес повторно.',

                'Тогда подскажите, какой у Вас вес ещё раз?'
            ]
        )
        context.set_state(MainGroup.Water.state_1)
    return resp
