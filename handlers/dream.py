import random

from tools import any_from
from typing_ import Response, AliceUserRequest, ResponseField
from fsm import FSMContext
from tools.time_parsing import parse_time, iter_go_sleep_time

from states import MainGroup


def dream_handler(context: FSMContext, req: AliceUserRequest, resp: dict | Response) -> dict | Response:
    if context.state == MainGroup.Dream.state_1:
        try:
            time = parse_time(req.request.command)
        except RuntimeError:
            resp.response = ResponseField(
                text='Извините, не поняла вас. Пожалуйста, повторите: во сколько вы планируете проснуться? Если это '
                     'повторяется не в первый раз, пожалуйста, попробуйте узвучить время в другом виде.'
            )
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
            except Exception:
                resp.response = ResponseField(
                    text='Извините, не поняла вас. Пожалуйста, повторите: во сколько вы планируете проснуться? Если это '
                         'повторяется не в первый раз, пожалуйста, попробуйте узвучить время в другом виде.'
                )

    elif context.state == MainGroup.Dream.end and any_from('ещё', 'еще', 'снов', 'рас', in_=req.request.command):
        resp.response = ResponseField(
            text=[
                'В какое время Вам необходимо проснуться?',
                'Подскажите повторно время, в которое Вам необходимо проснуться?'
            ],
        )
        MainGroup.Dream.state_1.set(context)

    return resp
