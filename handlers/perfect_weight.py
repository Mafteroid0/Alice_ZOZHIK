import random

from typing_ import Response, AliceUserRequest
from fsm import FSMContext
from tools import any_from

from states import MainGroup


def weight_handler(context: FSMContext, req: AliceUserRequest, resp: dict | Response) -> dict | Response:
    state = context.state
    command = req.request.command

    if state == MainGroup.Weight.state_1:
        if any_from('муж', 'мал', 'джен', in_=command):
            sex = 'male'

        elif any_from('жен', 'дев', 'лед', in_=command):
            sex = 'female'
        answer_options = ['Также для вычислений мне необходимо знать Ваш рост. Подскажите мне его, пожалуйста.', 'Чтобы подсказать вам идеальный вес, мне нужен ваш рост. Подскажите мне его, пожалуйста.',
                          'Подскажите Ваш рост и я с радостью рассчитаю Ваш рекомендованный вес.', 'Также для вычислений мне необходимо знать Ваш рост. Подскажите мне его, пожалуйста.']
        resp.update({
                    'response': {
                        'text': f'{random.choice(answer_options)}'
                    }
                })

        # st = command.replace(',', '.')
        # li = st.split(' ')
        # for el in li:
        #     el = el.replace(',', '.')
        #     if el.replace('.', '').isdecimal() and el.count('.') <= 1:
        #         answer_options = [
        #             f'Ваше минимальное потребление воды {float(el) * 30} миллилитров в день 💦',
        #
        #             f'Вам необходимо {float(el) * 30} миллилитров воды 🌊 в день, для хорошего метаболизма. ']
        #         resp.update({
        #             'response': {
        #                 'text': f'{random.choice(answer_options)}',
        #                 'card': {
        #                     'type': 'ItemsList',
        #                     'header': {
        #                         'text': f'{random.choice(answer_options)}'
        #                     },
        #                     'items': [
        #                         {"title": 'Рассчитать ещё раз', 'button': {"text": 'Рассчитать ещё раз'},
        #                          "description": 'описание...', "image_id": '997614/15f977696a281092bcc0'},
        #                         {"title": 'Вернуться к основному списку', "button": {"text": 'Назад'},
        #                          "description": 'описание...', "image_id": '1030494/cc3631c8499cdc8daf8b'}
        #
        #                     ]
        #                 }
        #             }
        #         })
        #         context.set_state(MainGroup.Water.end)
        #         break
            else:
                resp.update({
                    'response': {
                        'text': f'Не совсем поняла вас, повторите снова'
                    }
                })
    elif state == MainGroup.Water.end and \
            ('ещё' in command or 'счит' in command):
        resp.update({
            'response': {
                'text': 'Скажите свой вес в килограммах'
            }
        })
        context.set_state(MainGroup.Water.state_1)
    return resp
