import random

from tools import any_from
from typing_ import Response, AliceUserRequest, ResponseField
from fsm import FSMContext
from tools.time_parsing import parse_time, iter_go_sleep_time
from logging_ import logger

from states import MainGroup


def process_time_parsing_error(context: FSMContext, req: AliceUserRequest, resp: dict | Response) -> dict | Response:
    texts = (
        'Извините, не поняла вас. Пожалуйста, повторите: во сколько вы планируете проснуться?',

        'Извините, не поняла вас. Пожалуйста, повторите: во сколько вы планируете проснуться? '
        'Попробуйте перефразировать время пробуждения.',

        'Извините, не поняла вас. Пожалуйста, повторите: во сколько вы планируете проснуться? '
        'Попробуйте произнести время пробуждения в формате 12:34.'
    )

    errors_count = context.data.get('errors_count', 0)

    resp.response = ResponseField(
        text=texts[errors_count]
    )
    context.update_data(errors_count=errors_count + 1)

    return resp


def dream_handler(context: FSMContext, req: AliceUserRequest, resp: dict | Response) -> dict | Response:
    if context.state == MainGroup.Dream.state_1:
        try:
            time = parse_time(req.request.command)
        except RuntimeError as e:
            logger.exception(f'{e}')
            resp.response = ResponseField(
                text='Извините, не поняла вас. Пожалуйста, повторите: во сколько вы планируете проснуться? Попробуйте перефразировать время пробуждения. Лучше всего будет сказать его по шаблону 12:34',
                tts='Извините, не поняла вас. Пожалуйста, повторите: во сколько вы планируете проснуться? Попробуйте перефразировать время пробуждения. Лучше всего будет сказать его по шаблону двенадцать тридцать четыре'
            )  # TODO: Интегрировать это в process_time_parsing_error
        else:
            try:
                go_sleep_times = list(iter_go_sleep_time(time))
                print(time)
                print(go_sleep_times)
                answer_options = [
                    f'Чтобы быть полным сил после пробуждения, Вам следует лечь спать в {go_sleep_times[0].strftime("%H:%M")} '
                    f'или в {go_sleep_times[1].strftime("%H:%M")}😴. Не забудьте завести будильник!',

                    f'Ложитесь спать в {go_sleep_times[0].strftime("%H:%M")} или в {go_sleep_times[1].strftime("%H:%M")}, '
                    f'чтобы утром чувствовать себя полным сил. Не забудьте завести будильник!']
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
                                 "description": '', "image_id": '997614/15f977696a281092bcc0'},
                                {"title": 'Вернуться к основному списку', "button": {"text": 'Назад'},
                                 "description": '', "image_id": '1030494/cc3631c8499cdc8daf8b'}
                            ]
                        }
                    }
                })
                MainGroup.Dream.end.set(context)
            except Exception as e:
                logger.exception(f'{e}')
                process_time_parsing_error(context, req, resp)
            else:
                context.update_data(errors_count=0)

    elif context.state == MainGroup.Dream.end and any_from('ещё', 'еще', 'снов', 'рас', in_=req.request.command):
        resp.response = ResponseField(
            text=[
                'В какое время Вам необходимо проснуться?',
                'Подскажите повторно время, в которое Вам необходимо проснуться?'
            ],
        )
        MainGroup.Dream.state_1.set(context)

    return resp
