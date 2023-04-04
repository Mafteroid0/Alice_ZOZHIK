import random

from typing_ import Response, AliceUserRequest, ResponseField
from fsm import FSMContext
from tools import any_from

from states import MainGroup


def weight_handler(context: FSMContext, req: AliceUserRequest, resp: dict | Response) -> dict | Response:
    state = context.state
    command = req.request.command
    sex = 'female'

    if state == MainGroup.Weight.state_1:
        if any_from('муж', 'мал', 'джен', in_=command):
            sex = 'male'
            answer_options = ['Также для вычислений мне необходимо знать Ваш рост. Подскажите мне его, пожалуйста.',
                              'Подскажите Ваш рост и я с радостью рассчитаю Ваш рекомендованный вес.',

                              'Чтобы посчитать ваш идеальный вес, мне нужен ваш рост. Подскажите мне его, пожалуйста.']
            resp.response = ResponseField(
                text=f'{random.choice(answer_options)} \nРост указывайте в сантиметрах!'
            )
            context.set_state(MainGroup.Weight.sex_choose)

        elif any_from('жен', 'дев', 'лед', in_=command):
            sex = 'female'
            answer_options = ['Подскажите Ваш рост и я с радостью рассчитаю Ваш рекомендованный вес.',

                              'Также для вычислений мне необходимо знать Ваш рост. Подскажите мне его, пожалуйста.']
            resp.response = ResponseField(
                text=f'{random.choice(answer_options)} \nРост указывайте в сантиметрах!'
            )
            context.set_state(MainGroup.Weight.sex_choose)
        else:
            resp.update({
                'response': {
                    'text': f'Мне нужно знать ваш пол для более точного анализа. Давайте попробуем ещё раз: мужской или женский?',
                    'card': {
                        'type': 'ItemsList',
                        'header': {
                            'text': 'Выберите свой пол'
                        },
                        'items': [
                            {"title": 'Мужской', "button": {"text": 'Мужской'},
                             "image_id": '937455/de709f88951a3ae338fa'},
                            {"title": 'Женский', "button": {"text": 'Женский'},
                             "image_id": '937455/92fe9a7a01d9e788cfec'}

                        ]
                    },

                }
            })

    elif state == MainGroup.Weight.sex_choose:
        st = command.replace(',', '.')
        li = st.split(' ')
        for el in li:
            el = el.replace(',', '.')
            if el.replace('.', '').isdecimal() and el.count('.') <= 1 and float(el) >= 100:
                if sex == 'female':
                    verdict = round(49 + 1.7 * (0.394 * float(el) - 60), 1)
                else:  # sex == 'male'
                    verdict = round(52 + 1.9 * (0.394 * float(el) - 60), 1)

                answer_options = [
                    f'Ваш идеальный вес {verdict}кг. Что хотите сделать дальше: рассчитать рекомендуемое вес '
                    f'ещё раз или вернуться к основному списку?',
                    f'Ваш рекомендуемый вес {verdict}кг.'
                    f'Вы можете сделать расчёт ещё раз или вернуться к основному списку. Что выберете?']
                resp.update({
                    'response': {
                        'text': f'{random.choice(answer_options)}',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': f'{random.choice(answer_options)}'
                            },
                            'items': [
                                {"title": 'Рассчитать ещё раз', 'button': {"text": 'Рассчитать ещё раз'},
                                 "description": 'описание...', "image_id": '997614/15f977696a281092bcc0'},
                                {"title": 'Вернуться к основному списку', "button": {"text": 'Назад'},
                                 "description": 'описание...', "image_id": '1030494/cc3631c8499cdc8daf8b'}

                            ]
                        }
                    }
                })
                context.set_state(MainGroup.Weight.end)
                break
            else:
                resp.update({
                    'response': {
                        'text': f'Не совсем поняла вас, повторите снова. Учтите, что данный расчёт работает при росте более 100 сантиметров и возрасте старше пяти лет.'
                    }
                })
    elif state == MainGroup.Weight.end and \
            ('ещё' in command or 'счит' in command):
        resp.update({
            'response': {
                'text': f'Укажите свой пол',
                'card': {
                    'type': 'ItemsList',
                    'header': {
                        'text': 'Выберите свой пол'
                    },
                    'items': [
                        {"title": 'Мужской', "button": {"text": 'Мужской'},
                         "image_id": '937455/de709f88951a3ae338fa'},
                        {"title": 'Женский', "button": {"text": 'Женский'},
                         "image_id": '937455/92fe9a7a01d9e788cfec'}

                    ]
                },

            }
        })
        context.set_state(MainGroup.Weight.state_1)
    return resp
