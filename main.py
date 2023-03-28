import json
import random
import typing

from flask import Flask, request

from typing_ import AliceUserRequest
from fsm import StatesGroup, State, FSM
from time_parsing import parse_time, iter_go_sleep_time
from dialogs import warm_up_algorithm, warm_down_algorithm
from typing_ import TrainingStep

app = Flask(__name__)

fsm = FSM()


def dict_to_json(dict_: dict, *args, **kwargs):
    for key, value in dict_.items():
        try:
            dict_[key] = value.to_dict()
        except AttributeError:
            pass
    return json.dumps(dict_)


class MainGroup(StatesGroup):  # Состояние по умолчанию это None, его не нужно явно определять
    _fsm = fsm
    _help_message = 'Вам доступны следующие команды: "Я готов" (чтобы перейти к выбору тренировки или расчёту информации) и "Что ты умеешь?" (для уточнения моего функционала)'
    _default_state = None

    state_1 = State()

    class Water(StatesGroup):
        _help_message = 'Вы можете "Вернуться к основному списку", то есть в меню, или "Рассчитать ещё раз" и воспользоваться этой функцией повторно.'

        state_1 = State()
        end = State()

    class Dream(StatesGroup):
        _help_message = 'Вы можете "Вернуться к основному списку", то есть в меню, или "Рассчитать ещё раз" и воспользоваться этой функцией повторно.'

        state_1 = State()
        end = State()

    class Sport(StatesGroup):
        _help_message = 'Вам доступны команды: "Подробнее" (чтобы узнать правильную технику выполнения), "Выполнить упражнение" (чтобы начать тренироваться) и "Пропустить упражнение" (чтобы перейти к следующему упражнению в текущей тренировке)'

        class Wrap(StatesGroup):
            _help_message = ''

            class WarmUp(StatesGroup):
                _help_message = ''

                qw = State(_help_message='Вы можете перейти к разминке командой "Поехали". Также вы можете пропустить зарядку командой "К тренировке"')
                start = State(_help_message='Вы можете перейти к разминке командой "Поехали". Также вы можете пропустить зарядку командой "К тренировке"')

                task = State()

                end = State()

            class WarmDown(StatesGroup):
                _help_message = ''

                qw = State(_help_message='Вы можете перейти к заминке командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                start = State(_help_message='Вы можете перейти к заминке командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')

                task = State()

                end = State()

        state_home = State()

        class Power(StatesGroup):
            _help_message = ''

            state_1 = State(
                _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
            start = State(
                _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
            task1 = State()
            task1_help = State()
            task1_do = State()
            task2 = State()
            task2_help = State()
            task2_do = State()
            task3 = State()
            task3_help = State()
            task3_do = State()
            task4 = State()
            task4_help = State()
            task4_do = State()
            task5 = State()
            task5_help = State()
            task5_do = State()
            task6 = State()
            task6_help = State()
            task6_do = State()
            task7 = State()
            task7_help = State()
            task7_do = State()
            task8 = State()
            task8_help = State()
            task8_do = State()
            end = State()
            final = State()

        class Cardio(StatesGroup):
            _help_message = 'Вас есть выбор между классической (вызывается командой "классическая") и тренировкой с дополнительным инвентарём в виде скакалки (команда - "Со скакалкой")'

            state_1 = State(_help_message='У Вас есть выбор между классической (вызывается командой "классическая") и тренировкой с дополнительным инвентарём в виде скакалки (команда - "Со скакалкой")')

            class Solo(StatesGroup):
                _help_message = ''

                state_1 = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                start = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1 = State()
                task1_help = State()
                task1_do = State()
                task2 = State()
                task2_help = State()
                task2_do = State()
                task3 = State()
                task3_help = State()
                task3_do = State()
                task4 = State()
                task4_help = State()
                task4_do = State()
                task5 = State()
                task5_help = State()
                task5_do = State()
                task6 = State()
                task6_help = State()
                task6_do = State()
                task7 = State()
                task7_help = State()
                task7_do = State()
                task8 = State()
                task8_help = State()
                task8_do = State()
                task9 = State()
                task9_help = State()
                task9_do = State()
                final = State(_help_message='Вы можете "Повторить тренировку" или "Завершить тренировку"')

            class Rope(StatesGroup):
                _help_message = ''

                state_1 = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                start = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1 = State()
                task1_help = State()
                task1_do = State()
                task2 = State()
                task2_help = State()
                task2_do = State()
                task3 = State()
                task3_help = State()
                task3_do = State()
                task4 = State()
                task4_help = State()
                task4_do = State()
                task5 = State()
                task5_help = State()
                task5_do = State()
                end = State()
                final = State(_help_message='Вы можете "Повторить тренировку" или "Завершить тренировку"')

        class Zaradka(StatesGroup):
            _help_message = ''

            state_1 = State(_help_message='используйте одну из команд "5-минутная" или "10-минутная";')

            class Five(StatesGroup):
                _help_message = ''

                start = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1 = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1_help = State()
                task1_do = State()
                task2 = State()
                task2_help = State()
                task2_do = State()
                task3 = State()
                task3_help = State()
                task3_do = State()
                task4 = State()
                task4_help = State()
                task4_do = State()
                task5 = State()
                task5_help = State()
                task5_do = State()
                end = State()
                final = State(_help_message='Вы можете "Повторить тренировку" или "Завершить тренировку"')

            class Ten(StatesGroup):
                _help_message = ''

                start = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1 = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Поехали". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1_help = State()
                task1_do = State()
                task2 = State()
                task2_help = State()
                task2_do = State()
                task3 = State()
                task3_help = State()
                task3_do = State()
                task4 = State()
                task4_help = State()
                task4_do = State()
                task5 = State()
                task5_help = State()
                task5_do = State()
                task6 = State()
                task6_help = State()
                task6_do = State()
                task7 = State()
                task7_help = State()
                task7_do = State()
                task8 = State()
                task8_help = State()
                task8_do = State()
                task9 = State()
                task9_help = State()
                task9_do = State()
                task10 = State()
                task10_help = State()
                task10_do = State()
                end = State()
                final = State(_help_message='Вы можете "Повторить тренировку" или "Завершить тренировку"')


# Шаблон для условий:  if state == MyStates.state_1
# Диаграмма: https://miro.com/app/board/uXjVMdrXZW0=/


def is_positive(command: str) -> bool:
    return 'готов' in command or 'погн' in command or 'поехали' in command or 'давай' in command or 'да' in command or 'выполн' in command or 'запус' in command


def start_power_training(user_id: str, resp: dict) -> dict:
    resp.update({
        'response': {
            'text': 'Давайте приступим к силовой тренировке. Для нее Вам нужен только боевой настрой. Одно упражнение длится 40 секунд. '
                    'Перед  его выполнением Вы можете изучить упражнение подробнее, начать делать его или пропустить выполнение и перейти к следующему.'
                    'Вы готовы к силовой тренировке или подберём Вам что-нибудь другое?'
                    'Вы готовы начать, или рассмотрим другую тренировку?',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Комментарий: Если на этот этап мы перешли с разминки, то об этом будет написано'
                            'Приступаем к выполнению силовой тренировки.'
                },
                'items': [
                    {"title": 'Я готов', "button": {"text": 'Я готов'},
                     "image_id": '997614/72ab6692a3db3f4e3056'},
                    {"title": 'Выберем другую тренировку',
                     "button": {"text": 'Выберем другую тренировку'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}

                ]
            }

        }
    })
    fsm.set_state(user_id, MainGroup.Sport.Power.start)
    return resp


def start_warmup(user_id: str, resp: dict) -> dict:
    resp.update({
        'response': {
            'text': 'Во время тренировки Вы можете изучить упражнение подробнее, начать выполнять его или '
                    'пропустить текущее упражнение и перейти к следующему.\n'
                    'Вы готовы начать или выберем другую тренировку?',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Приступаем к выполнению разминки'
                },
                'items': [
                    {"title": 'Я готов', "button": {"text": 'Я готов'},
                     "image_id": '997614/72ab6692a3db3f4e3056'},
                    {"title": 'Пропустить',
                     "button": {"text": 'Пропустить'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}
                ]
            }
        }
    })
    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmUp.start)
    return resp


def start_solo_cardio(user_id: str, resp: dict) -> dict:
    resp.update({
        'response': {
            'text': 'Давайте приступим к кардиотренировке. Для нее вам не понадобится дополнительный инвентарь,'
                    ' не забудьте взять только хорошее настроение и правильный настрой. На каждое упражнение у вас уйдёт по 40 секунд. '
                    'Во время тренировки вы можете изучить упражнение подробнее, выполнить его, или пропустить выполнение и перейти к следующему. '
                    'Вы готовы начать, или рассмотрим другую тренировку?',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Приступаем к выполнению кардиотренировки'
                },
                'items': [
                    {"title": 'Я готов', "button": {"text": 'Я готов'},
                     "image_id": '997614/72ab6692a3db3f4e3056'},
                    {"title": 'Выберем другую тренировку',
                     "button": {"text": 'Выберем другую тренировку'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}

                ]
            }

        }
    })
    fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.start)
    return resp


def start_rope_cardio(user_id: str, resp: dict) -> dict:
    resp.update({
        'response': {
            'text': 'Давайте приступим к кардиотренировке. Для нее Вам понадобится только скакалка и хорошее настроение.'
                    ' Одно упражнение занимает 40 секунд. Перед тем, как его проделать, Вы можете изучить технику подробнее,'
                    ' начать выполнение или пропустить его и перейти к следующему.Вы готовы к кардио или подберём другую тренировку?',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Приступаем к выполнению скардиотренировки'
                },
                'items': [
                    {"title": 'Я готов', "button": {"text": 'Я готов'},
                     "image_id": '997614/72ab6692a3db3f4e3056'},
                    {"title": 'Выберем другую тренировку',
                     "button": {"text": 'Выберем другую тренировку'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}

                ]
            }

        }
    })
    fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.start)
    return resp


def end_warmup(user_id: str, resp: dict) -> dict:  # Возврат к упражнению которое было до начала разминки
    resp.update({
        'response': {
            'text': 'Вы хорошо потрудились, поздравляю вас с победой! Что выберите дальше: скажите "повторить разминку", чтобы потренироваться ещё раз или "к тренировке", чтобы начать основную тренировку?',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Повторим разминку или перейдём к основной тренировке?'
                },
                'items': [
                    {"title": 'Повторить разминку', "button": {"text": 'Повторить разминку'},
                     "image_id": '997614/15f977696a281092bcc0'},
                    {"title": 'К тренировке',
                     "button": {"text": 'К тренировке'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}
                ]
            }

        }
    })

    fsm.update_data(user_id, step=0)
    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmUp.end)

    return resp


def cancel_warmup(user_id: str, resp: dict, data: dict | None = None) -> dict:
    if data is None:
        data = fsm.get_data(user_id)

    return data['callback'](user_id, resp)


def any_from(l: typing.Sequence[str], *, in_: str):
    return any((i in in_ for i in l))


def start_session(user_id: str, resp: dict, add_help_button: bool = True) -> dict:
    # Действия при новой сессии
    answer_options = ['Привет🖐!  Всегда хотели окунуться в мир здорового образа жизни? '
                      'Поздравляю, Вы сделали правильный выбор.'
                      'Я навык ... помогу освоить основы ЗОЖ на практике с лёгкостью и удовольствием.'
                      'Если хотите ознакомиться с моим функционалом, то скажите "Что ты умеешь?". '
                      'Если же готовы приступить, то скажите "Поехали".',

                      'Очень приятно осознавать, что Вы решили заботится о себе и своём здоровье💖!'
                      ' Я позабочусь о Вас и облегчу ваше знакомство с ЗОЖ. Вы сможете начать следить '
                      'за Вашим здоровьем с удовольствием.'
                      ' Если нужно ознакомиться с функционалом навыка, то скажите "Что ты умеешь?". '
                      'Если уже хотите приступить, то скажите "Поехали".']
    resp.update({
        'response': {
            'text': f'{random.choice(answer_options)}.\n#Комментарии для проверяющих будут обозначены знаком хештега для удобства#',
            'buttons': [
                {
                    'title': 'Что ты умеешь?',
                    'hide': True
                },
                {
                    "title": "Поехали!",
                    "hide": True
                }
            ]
        }
    })
    if add_help_button:
        resp['response']['buttons'].append({
            'title': 'Помощь',
            'hide': False
        })
    fsm.reset_state(user_id, with_data=True)
    return resp


def start_warmdown(user_id: str, resp: dict) -> dict:
    resp.update({
        'response': {
            'text': 'Во время тренировки Вы можете изучить упражнение подробнее, '
                    'начать выполнять его или пропустить текущее упражнение и перейти к следующему.\n'
                    'Вы готовы начать или выберем другую тренировку?',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Приступаем к выполнению заминки'
                },
                'items': [
                    {"title": 'Я готов', "button": {"text": 'Я готов'},
                     "image_id": '997614/72ab6692a3db3f4e3056'},
                    {"title": 'Пропустить',
                     "button": {"text": 'Пропустить'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}
                ]
            }
        }
    })
    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmDown.start)
    return resp


def end_warmdown(user_id: str, resp: dict) -> dict:  # Возврат к упражнению которое было до начала разминки
    resp.update({
        'response': {
            'text': 'Вы хорошо потрудились, поздравляю вас с  очередной победой! Что выберите дальше: '
                    'скажите "повторить заминку" или "завершить заминку"?',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Повторим зазминку или перейдём к основному списку?'
                },
                'items': [
                    {"title": 'Повторить разминку', "button": {"text": 'Повторить разминку'},
                     "image_id": '997614/15f977696a281092bcc0'},
                    {"title": 'Вернуться к основному списку',
                     "button": {"text": 'Назад'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}
                ]
            }

        }
    })

    fsm.update_data(user_id, step=0)
    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmDown.end)

    return resp


def cancel_warmdown(user_id: str, resp: dict, data: dict | None = None) -> dict:
    if data is None:
        data = fsm.get_data(user_id)

    return data['callback'](user_id, resp)


def finish_solo_cardio(user_id: str, resp: dict) -> dict:
    resp.update({
        'response': {
            'text': 'Вы хорошо потрудились, горжусь Вами. Повторим тренировку или вернёмся в меню? Выбор за Вами.',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Повторим тренировку или вернёмся в меню?'
                },
                'items': [
                    {"title": 'Повторить тренировку', "button": {"text": 'Повторить тренировку'},
                     "image_id": '997614/15f977696a281092bcc0'},
                    {"title": 'Вернуться в меню',
                     "button": {"text": 'Вернуться в меню'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}

                ]
            }

        }
    })
    fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.final)
    return resp


def finish_rope_cardio(user_id: str, resp: dict) -> dict:
    resp.update({
        'response': {
            'text': 'Вы хорошо потрудились, горжусь Вами. Повторим тренировку или вернёмся в меню? Выбор за Вами.',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Повторим тренировку или вернёмся в меню?'
                },
                'items': [
                    {"title": 'Повторить тренировку', "button": {"text": 'Повторить тренировку'},
                     "image_id": '997614/15f977696a281092bcc0'},
                    {"title": 'Вернуться в меню',
                     "button": {"text": 'Вернуться в меню'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}

                ]
            }

        }
    })
    fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.final)
    return resp


def finish_power_training(user_id: str, resp: dict) -> dict:
    resp.update({
        'response': {
            'text': 'Вы хорошо потрудились, горжусь Вами. Повторим тренировку или вернёмся в меню? Выбор за Вами.',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Повторим тренировку или вернёмся в меню?'
                },
                'items': [
                    {"title": 'Повторить тренировку', "button": {"text": 'Повторить тренировку'},
                     "image_id": '997614/15f977696a281092bcc0'},
                    {"title": 'Вернуться в меню',
                     "button": {"text": 'Вернуться в меню'},
                     "image_id": '1030494/cc3631c8499cdc8daf8b'}

                ]
            }

        }
    })
    fsm.set_state(user_id, MainGroup.Sport.Power.final)
    return resp


@app.route('/alice', methods=['POST'])
def main():  # event, context
    tracks_fourteen = [
        '<speaker audio="dialogs-upload/063cdddd-d9f0-40a7-9fa8-ff5ab745aa44/bd88f1cd-426b-430f-adc4-e66d4f19549d.opus">',
        '<speaker audio="dialogs-upload/063cdddd-d9f0-40a7-9fa8-ff5ab745aa44/047165c7-4a08-4426-ade7-ce961e87aad1.opus">',
        '<speaker audio="dialogs-upload/063cdddd-d9f0-40a7-9fa8-ff5ab745aa44/e7178478-0cca-4b0e-bba9-cd6cd2109d73.opus">']
    tracks_sixteen = [
        '<speaker audio="dialogs-upload/063cdddd-d9f0-40a7-9fa8-ff5ab745aa44/4e7a987a-48cc-4ca3-8add-fa34a96852b2.opus">',
        '<speaker audio="dialogs-upload/063cdddd-d9f0-40a7-9fa8-ff5ab745aa44/cce10ad9-c6be-46ec-a0e0-1897db4841e3.opus">',
        '<speaker audio="dialogs-upload/063cdddd-d9f0-40a7-9fa8-ff5ab745aa44/471315ec-dbf4-4821-ac6d-9171af52f3f9.opus">']
    req = AliceUserRequest(request.data.decode())
    motivations = ['Удачи! #в данный момент проигрывается трек#', 'Так держать! #в данный момент проигрывается трек#',
                   'Вы справитесь! #в данный момент проигрывается трек#']
    command = req.request.command
    user_id = req.session.user.user_id
    state = fsm.get_state(user_id)

    resp = {'version': req.version,
            'session': req.session}

    print(f'{state=}')
    print(f'data={fsm.get_data(user_id)}')
    if req.session.new:
        resp = start_session(user_id, resp)
        return dict_to_json(resp, ensure_ascii=False, indent=2)

    print(command)
    if any_from(('помо', 'help'), in_=command):
        print({'text': state.help_message if state is not None else MainGroup.help_message,
                                  'buttons': fsm.get_data(user_id).get('buttons', [])})
        # resp = start_session(user_id, resp, add_help_button=False)
        resp.update({'response': {'text': state.help_message if state is not None else MainGroup.help_message,
                                  'buttons': fsm.get_data(user_id).get('buttons', [])}})
        #                                    'Не беспокойтесь я подскажу Вам, что делать в зависимости от того, где Вы сейчас находитесь. Если Вы сейчас ...\n'
        #                                  'На этапе приветствия, то Вам доступны следующие команды: "Я готов" (чтобы перейти к выбору тренировки или расчёту информации)'
        #                                  ' и "Что ты умеешь?" (для уточнения моего функционала);\n'
        #                                  'Узнавали Ваше дневное потребление воды, подсчитывали фазы сна или идеальный вес, '
        #                                  'то далее Вы можете "Вернуться к основному списку", то есть в меню, или "Рассчитать ещё раз" и воспользоваться тем же навыком повторно.начинаете приступать к тренировке, то перейти к'
        #                                  ' выполнению Вы можете командой "Поехали". Также можно вернуться обратно к выбору командой "Вернуться к основному списку";\n'
        #                                  'Выполняете упражнение внутри тренировки, разминки или заминки, то Вам доступны команды: "Подробнее" (чтобы узнать правильную технику выполнения), "Выполнить упражнение" '
        #                                  '(чтобы начать тренироваться) и "Пропустить упражнение" (чтобы перейти к следующему упражнению в текущей тренировке);\n'
        #                                  'Закончили тренировку, то можно "Повторить тренировку" или "Завершить тренировку";\nВыбираете тип кардиотренировки, то у Вас есть выбор между классической '
        #                                  '(вызывается командой "классическая") и тренировкой с дополнительным инвентарём в виде скакалки (команда - "Со скакалкой");\n'
        #                                  'Выбираете тип зарядки, то используйте одну из команд "5-минутная" или "10-минутная";\n'
        #                                  'Начинаете расчёт идеального веса и Вас просят указать пол, то скажите "мужской" или "женский".Также перед и после тренировок Вам будет предложено выполнить разминку и заминку соответственно '
        #                                  'согласить или отказаться их выполнять Вы можете с помощью простых команд "да" и "нет".'

    elif state is None and (command == 'что ты умеешь'):
        answer_options = ['Очень здорово, что вы спросили меня про это. В мой функционал входит:\n'
                          '🧘‍♂️ Утренняя зарядка\n'
                          '🏃‍♂️ Кардиотренировка\n'
                          '🏋️‍♀️ Силовая фуллбади тренировка\n'
                          '😴 Фазы сна\n'
                          '🥛 Водный баланс\n'
                          'К каждому упражнению есть описание и GIF, наглядно показывающий, как правильно выполнять упражнение. Чтобы перейти к списку, скажите Поехали.',

                          'Я рада, что вы решили спросить меня об этом. Если говорить вкратце, то в мой функционал входит:\n'
                          '🧘‍♂️ Утренняя зарядка\n'
                          '🏃‍♂️ Кардиотренировка\n'
                          '🏋️‍♀️ Силовая фуллбади тренировка\n'
                          '😴 Фазы сна\n'
                          '🥛 Водный баланс\n'
                          'К каждому из упражнений будет предоставлено описание и GIF, наглядно демонстрирующий , как выполнять упражнение. Чтобы перейти к списку, скажите "Поехали".']

        resp.update({
            'response': {
                'text': f'{random.choice(answer_options)} \n',
                'buttons': [
                    {
                        'title': 'Поехали!',
                        'hide': True
                    },
                    {
                        'title': 'Помощь',
                        'hide': False
                    }
                ]

            }
        })
        fsm.set_state(user_id, MainGroup.state_1)
        return dict_to_json(resp, ensure_ascii=False, indent=2)

    elif (state in (MainGroup.state_1, None)) and (
            'поехали' in command or 'нач' in command):  # TODO: Добавить в условия номера стейтов, из которых можно сюда попасть (см. диаграмму)
        # answer_options = ['Вау, Вы уже в нескольких шагах от здорового образа жизни очень рада за Вас 😍. '
        #                   'Для начала выберите, чем хотите заняться или что Вам нужно узнать:'
        #                   ' "Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".',
        #
        #                   'Вы уже совсем-совсем близко к здоровой жизни 😍, горжусь Вами. '
        #                   'Время выбирать, чем хотите заняться или что Вам нужно узнать:\n'
        #                   '"Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".']

        resp.update({
            'response': {
                'text': 'Это сообщение никто не увидит :(',
                'tts': f'Вы уже в нескольких шагах от здорового образа жизни! Чем сегодня займёмся? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", "Идеальный вес", или "Фазы сна".',
                'card': {
                    'type': 'ItemsList',
                    'header': {
                        'text': 'Чем сегодня займёмся? Выбирайте: #Кнопка "идеальный вес" временно недоступна# '
                    },
                    'items': [
                        {"title": 'кардиотренировка', 'button': {"text": 'кардиотренировка'},
                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                        {"title": 'силовая тренировка', "button": {"text": 'силовая тренировка'},
                         "description": 'описание...', "image_id": '1533899/f030bee0ec7edea516e3'},
                        {"title": 'утренняя зарядка', "button": {"text": 'утренняя зарядка'},
                         "description": 'описание...', "image_id": '1540737/cc26a14712e6995a6624'},
                        {"title": 'водный баланс', "button": {"text": 'водный баланс'}, "description": 'описание...',
                         "image_id": '1540737/dc7c3c075dd3ecc22fc7'},
                        {"title": 'фазы сна', "button": {"text": 'фазы сна'}, "description": 'описание...',
                         "image_id": '213044/e81c096eeedd03ef9a2e'}

                    ]
                }
            }
        })
        fsm.reset_state(user_id, with_data=True)
        fsm.set_state(user_id, MainGroup.Sport.state_home)

    elif state in MainGroup:
        if 'вернуться' in command or 'назад' in command or 'основ' in command or 'домой' in command or 'начало' in command:
            print(1)
            resp.update({
                'response': {
                    'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", "Идеальный вес", или "Фазы сна".',
                    'card': {
                        'type': 'ItemsList',
                        'header': {
                            'text': 'Чем займёмся на этот раз? #Кнопка "идеальный вес" временно недоступна#'
                        },
                        'items': [
                            {"title": 'кардиотренировка', 'button': {"text": 'кардиотренировка'},
                             "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                            {"title": 'силовая тренировка', "button": {"text": 'силовая тренировка'},
                             "description": 'описание...', "image_id": '1533899/f030bee0ec7edea516e3'},
                            {"title": 'утренняя зарядка', "button": {"text": 'утренняя зарядка'},
                             "description": 'описание...', "image_id": '1540737/cc26a14712e6995a6624'},
                            {"title": 'водный баланс', "button": {"text": 'водный баланс'},
                             "description": 'описание...', "image_id": '1540737/dc7c3c075dd3ecc22fc7'},
                            {"title": 'фазы сна', "button": {"text": 'фазы сна'}, "description": 'описание...',
                             "image_id": '213044/e81c096eeedd03ef9a2e'}

                        ]
                    }
                }
            })
            fsm.set_state(user_id, MainGroup.Sport.state_home)
        elif state == MainGroup.Sport.state_home:
            if 'вод' in command or 'баланс' in command:
                answer_options = [
                    'Вода жизненно необходима каждому человеку, а употребление её дневной нормы улучшает метаболизм. Я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. Подскажите, пожалуйста, Ваш вес.',

                    'Так как мы состоим из воды примерно на 70% 🐳, то употреблять её в достаточном количестве очень важно. '
                    'Не переживайте 😉 , я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. '
                    'Для того, чтобы точно рассчитать минимальное объём воды, мне нужен вес человека. Подскажите, пожалуйста, вес Вашего тела в килограммах.']

                resp.update({
                    'response': {
                        'text': f'{random.choice(answer_options)}'
                    }
                })
                fsm.set_state(user_id, MainGroup.Water.state_1)

            elif 'сон' in command or 'сна' in command or 'фаз' in command:
                resp.update({
                    'response': {
                        'text': 'Здорово🥰 , что Вы решили следить за своим сном, так как он играет важную роль в нашей жизни 🛌.'
                                'Напишите, во сколько вы хотите проснуться,'
                                ' а я Вам подскажу идеальное время, когда необходимо будет лечь спать, чтобы встать бодрым.'
                    }
                })
                fsm.set_state(user_id, MainGroup.Dream.state_1)
                print('SON?')

            elif 'сил' in command:
                answer_options = [
                    'Замечательно! Кардиотренировки несут огромную пользу, а также поднимают настроение. Выберите тип кардио:  классическая или со скакалкой.',

                    'Прекрасный выбор😍! Нагружая сердечно-сосудистую систему, мы укрепляем здоровье. Выберите тип кардио: классическая или со скакалкой.']
                resp.update({
                    'response': {
                        'text': 'Хотите выполнить разминку перед тренировкой?',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': 'Хотите выполнить разминку? #Кнопка "идеальный вес" временно недоступна#'
                            },
                            'items': [
                                {"title": 'Выполнить разминку', "button": {"text": 'Да'},
                                 "image_id": '213044/9c13b9b997d78cde2579'},
                                {"title": 'Продолжить без разминки', "button": {"text": 'Нет'},
                                 "image_id": '1540737/cc47e154fc7c83b6ba0d'}

                            ]
                        }

                    }
                })
                fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmUp.qw)
                fsm.update_data(user_id, callback=start_power_training)

            elif 'кард' in command:
                answer_options = [
                    'Замечательно! Кардиотренировки несут огромную пользу, а также поднимают настроение. Выберите тип кардио:  классическая или со скакалкой.',

                    'Прекрасный выбор😍! Нагружая сердечно-сосудистую систему, мы укрепляем здоровье. Выберите тип кардио: классическая или со скакалкой.']
                resp.update({
                    'version': req['version'],
                    'session': req['session'],
                    'response': {
                        'text': f'{random.choice(answer_options)}',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': 'Выберите тип кардио'
                            },
                            'items': [
                                {"title": 'Классическая', "button": {"text": 'Классическая'},
                                 "image_id": '1533899/13a130643a2fcdac537a'},
                                {"title": 'Со скакалкой', "button": {"text": 'Со скакалкой'},
                                 "image_id": '1540737/fa873a0d82d3696c73ff'}

                            ]
                        },

                    }
                })
                fsm.set_state(user_id, MainGroup.Sport.Cardio.state_1)

            elif 'заряд' in command:
                answer_options = [
                    'Прекрасно🔥\nДержать тело в форме необходимо всем, очень приятно, что Вы это понимаете. Однако зарядки тоже бывают разными. Какой тип зарядки выберите: 5-минутная или 10-минутная?',
                    'Отличный выбор🤩\nЗарядка нужна всем, но немногие это понимают, к счастью к Вам это не относится. Выберите тип зарядки: 5-минутная или 10-минутная.',
                    'Давайте вместе приведём Ваше тело в тонус. Выберите тип зарядки:  5-минутная или 10-минутная.']
                resp.update({
                    'response': {
                        'text': f'{random.choice(answer_options)}',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': 'Выберите тип зарядки'
                            },
                            'items': [
                                {"title": '5-минутная', "button": {"text": '5-минутная'},
                                 "image_id": '213044/99d6eb5c5125693a3154'},
                                {"title": '10-минутная', "button": {"text": '10-минутная'},
                                 "image_id": '997614/e024d33f7ffd1429b89c'}

                            ]
                        },

                    }
                })
                fsm.set_state(user_id, MainGroup.Sport.Zaradka.state_1)

            elif 'вес' in command:
                resp.update({
                    'response': {
                        'text': f'# К сожалению, наши программисты не успели доделать эту часть навыка😣\nНо не переживайте, совсем скоро эта функция станет доступна!\nСкажите "поехали" чтобы вернуться в главное меню. #'
                    }
                })
                fsm.set_state(user_id, MainGroup.state_1)

            else:
                resp.update({
                    'response': {
                        'text': 'Извините, не поняла вас😣\nДавайте попробуем заново выбрать занятие!\n'
                                '"Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", "Идеальный вес",или "Фазы сна".',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': 'Давайте попробуем заново выбрать занятие! #Кнопка "идеальный вес" временно недоступна#'
                            },
                            'items': [
                                {"title": 'кардиотренировка', 'button': {"text": 'кардиотренировка'},
                                 "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                {"title": 'силовая тренировка', "button": {"text": 'силовая тренировка'},
                                 "description": 'описание...', "image_id": '1533899/f030bee0ec7edea516e3'},
                                {"title": 'утренняя зарядка', "button": {"text": 'утренняя зарядка'},
                                 "description": 'описание...', "image_id": '1540737/cc26a14712e6995a6624'},
                                {"title": 'водный баланс', "button": {"text": 'водный баланс'},
                                 "description": 'описание...', "image_id": '1540737/dc7c3c075dd3ecc22fc7'},
                                {"title": 'фазы сна', "button": {"text": 'фазы сна'}, "description": 'описание...',
                                 "image_id": '213044/e81c096eeedd03ef9a2e'}

                            ]
                        }
                    }
                })
                fsm.set_state(user_id, MainGroup.Sport.state_home)
        elif state in MainGroup.Dream:
            if state == MainGroup.Dream.state_1:
                time = parse_time(command)
                go_sleep_times = list(iter_go_sleep_time(time))
                print(time)
                print(go_sleep_times)
                answer_options = [
                    f'Чтобы после сна чувствовать себя полным энергией, Вам следует лечь спать в {go_sleep_times[0].strftime("%H:%M")} '
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
                                 "description": 'описание...', "image_id": '997614/15f977696a281092bcc0'},
                                {"title": 'Вернуться к основному списку', "button": {"text": 'Назад'},
                                 "description": 'описание...', "image_id": '1030494/cc3631c8499cdc8daf8b'}

                            ]
                        }
                    }
                })
                fsm.set_state(user_id, MainGroup.Dream.end)
            elif state == MainGroup.Dream.end:
                resp.update({
                    'response': {
                        'text': 'Во сколько вы хотите проснуться?'
                    }
                })
                fsm.set_state(user_id, MainGroup.Dream.state_1)
        elif state in MainGroup.Water:
            if state == MainGroup.Water.state_1:
                st = command.replace(',', '.')
                li = st.split(' ')
                for el in li:
                    el = el.replace(',', '.')
                    if el.replace('.', '').isdecimal() and el.count('.') <= 1:
                        answer_options = [
                            f'Ваше минимальное потребление воды {float(el) * 30} миллилитров в день 💦',

                            f'Вам необходимо {float(el) * 30} миллилитров воды 🌊 в день, для хорошего метаболизма. ']
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
                        fsm.set_state(user_id, MainGroup.Water.end)
                        break
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
                fsm.set_state(user_id, MainGroup.Water.state_1)

        elif state in MainGroup.Sport.Cardio:
            if state == MainGroup.Sport.Cardio.state_1:
                resp.update({
                    'response': {
                        'text': 'Хотите выполнить разминку перед тренировкой?',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': 'Хотите выполнить разминку?'
                            },
                            'items': [
                                {"title": 'Выполнить разминку', "button": {"text": 'Да'},
                                 "image_id": '213044/9c13b9b997d78cde2579'},
                                {"title": 'Продолжить без разминки', "button": {"text": 'Нет'},
                                 "image_id": '1540737/cc47e154fc7c83b6ba0d'}

                            ]
                        }

                    }
                })
                if 'клас' in command or 'станд' in command or 'перв' in command or 'обычн' in command or 'без' in command:
                    fsm.update_data(user_id, callback=start_solo_cardio)
                    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmUp.qw)
                elif 'скак' in command or 'со' in command or 'втор' in command:
                    fsm.update_data(user_id, callback=start_rope_cardio)
                    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmUp.qw)
                else:
                    resp.update({
                        'response': {
                            'text': 'Повторите пожалуйста, какую именно кардиотренировку вы хотите выполнить: классическую или со скакалкой'
                            ,
                            'buttons': [
                                {
                                    'title': 'Классическая',
                                    'hide': True
                                },
                                {
                                    'title': 'Со скакалкой',
                                    'hide': True
                                }
                            ]

                        }
                    })

            elif state in MainGroup.Sport.Cardio.Solo:
                if state == MainGroup.Sport.Cardio.Solo.state_1:
                    pass
                    # if 'нет' in command or 'не ' in command:
                    #     start_solo_cardio()
                    # elif 'да' in command or 'конечн' in command:
                    #     fsm.set_state
                elif state in (MainGroup.Sport.Cardio.Solo.start, MainGroup.Sport.Cardio.Solo.final):
                    if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command:
                        print(2)
                        resp.update({
                            'response': {
                                'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", "Идеальный вес",или "Фазы сна".',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Чем займёмся на этот раз? #Кнопка "идеальный вес" временно недоступна#'
                                    },
                                    'items': [
                                        {"title": 'кардиотренировка', 'button': {"text": 'кардиотренировка'},
                                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                        {"title": 'силовая тренировка', "button": {"text": 'силовая тренировка'},
                                         "description": 'описание...', "image_id": '1533899/f030bee0ec7edea516e3'},
                                        {"title": 'утренняя зарядка', "button": {"text": 'утренняя зарядка'},
                                         "description": 'описание...', "image_id": '1540737/cc26a14712e6995a6624'},
                                        {"title": 'водный баланс', "button": {"text": 'водный баланс'},
                                         "description": 'описание...', "image_id": '1540737/dc7c3c075dd3ecc22fc7'},
                                        {"title": 'фазы сна', "button": {"text": 'фазы сна'},
                                         "description": 'описание...',
                                         "image_id": '213044/e81c096eeedd03ef9a2e'}

                                    ]
                                }
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.state_home)
                    elif 'да' in command or 'готов' in command or 'повтор' in command or 'нач' in command or 'запус' in command:
                        resp.update({
                            'response': {
                                'text': 'Начинаем первое упражнение!'
                                        'Поочерёдное сгибание ног с последующим подниманием коленей к груди',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '997614/15bfafd8b629b323890b',
                                    "title": 'Упражнение 1',
                                    "description": 'Поочерёдное сгибание ног с последующим подниманием коленей к груди'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task1)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение тренировки, или возвращаемся в меню?'
                                ,
                                'buttons': [
                                    {
                                        'title': 'Вернуться в меню',
                                        'hide': True
                                    },
                                    {
                                        'title': 'Запустить тренировку',
                                        'hide': True
                                    }
                                ]

                            }
                        })
                elif state in (
                        MainGroup.Sport.Cardio.Solo.task1, MainGroup.Sport.Cardio.Solo.task1_help,
                        MainGroup.Sport.Cardio.Solo.task1_do) or (
                        state == MainGroup.Sport.Cardio.Solo.final and 'повтор' in command):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Для первого упражнения встаньте прямо, соберите ноги вместе, согните руки. '
                                        'Поднимите одно колено к груди. Опустите ногу и повторите на другую сторону. Выполняйте руками движения бегуна.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task1_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task1_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task1_do, MainGroup.Sport.Cardio.Solo.task1_help,
                            MainGroup.Sport.Cardio.Solo.task1) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Увеличиваем интенсивность тренировки. Выполняем энергичные прыжки с поднятием рук.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/6cd05842046b48c768bc',
                                    "title": 'Упражнение 2',
                                    "description": 'Энергичные прыжки с поднятием рук.'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task2)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state in (
                        MainGroup.Sport.Cardio.Solo.task2, MainGroup.Sport.Cardio.Solo.task2_help,
                        MainGroup.Sport.Cardio.Solo.task2_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': ' Стопы поставьте плотно вместе, а руки вдоль туловища. Выполните два движения вместе:'
                                        ' в прыжке расставьте широко ноги и вытяните вверх руки, сводя их вместе над головой. Прыжком вернитесь в начальную позу.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task2_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task2_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task2_do, MainGroup.Sport.Cardio.Solo.task2_help,
                            MainGroup.Sport.Cardio.Solo.task2) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'У вас хорошо получается! Следующее упражнения - бег в планке',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1030494/94bcca53f06da5b24f90',
                                    "title": 'Упражнение 3',
                                    "description": 'Бег в планке'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task3)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state in (
                        MainGroup.Sport.Cardio.Solo.task3, MainGroup.Sport.Cardio.Solo.task3_help,
                        MainGroup.Sport.Cardio.Solo.task3_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': ' Для следующего упражнения встаньте в планку на прямых руках. Начните имитировать бег – по очереди подтягивайте колени к груди. Ноги ставьте на носки, линию позвоночника не меняйте.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task3_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task3_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task3_do, MainGroup.Sport.Cardio.Solo.task3_help,
                            MainGroup.Sport.Cardio.Solo.task3) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Приступаем к прыжкам в планке',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '213044/bf1b200f757b3aae40df',
                                    "title": 'Упражнение 4',
                                    "description": 'Прыжки в планке'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task4)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state in (
                        MainGroup.Sport.Cardio.Solo.task4, MainGroup.Sport.Cardio.Solo.task4_help,
                        MainGroup.Sport.Cardio.Solo.task4_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': ' Продолжайте стоять в планке. Для нового задания оттолкнитесь носками, разведите ноги в стороны, легким прыжком соберитесь обратно. Не прогибайтесь в спине, взгляд направлен вперед-вниз.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task4_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task4_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task4_do, MainGroup.Sport.Cardio.Solo.task4_help,
                            MainGroup.Sport.Cardio.Solo.task4) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Вы хорошо справляетесь! Далее прыжки из приседа. ',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '937455/b69ef8ea88fa63b48c20',
                                    "title": 'Упражнение 5',
                                    "description": 'прыжки из приседа.'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task5)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state in (
                        MainGroup.Sport.Cardio.Solo.task5, MainGroup.Sport.Cardio.Solo.task5_help,
                        MainGroup.Sport.Cardio.Solo.task5_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Начните из положения стоя, ноги на ширине плеч. Выполните приседание и выведите руки вперед. Выпрыгивайте, одновременно выпрямив руки.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task5_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task5_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task5_do, MainGroup.Sport.Cardio.Solo.task5_help,
                            MainGroup.Sport.Cardio.Solo.task5) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Не сбавляем темп тренировки 💪 Далее на очереди упражнение бёрпи. ',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '997614/538aaaa7db557abbda82',
                                    "title": 'Упражнение 6',
                                    "description": 'упражнение бёрпи.'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task6)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state in (
                        MainGroup.Sport.Cardio.Solo.task6, MainGroup.Sport.Cardio.Solo.task6_help,
                        MainGroup.Sport.Cardio.Solo.task6_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Подпрыгните, отведите ноги назад и опустите таз, чтобы получилась поза планки. Соберитесь обратно прыжком, выпрямитесь, руки вытяните вверх.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task6_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task6_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task6_do, MainGroup.Sport.Cardio.Solo.task6_help,
                            MainGroup.Sport.Cardio.Solo.task6) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Следующее энергичное упражнение - велосипед.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '997614/1ef3a8d9152694fe40e3',
                                    "title": 'Упражнение 7',
                                    "description": 'Велосипед'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task7)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state in (
                        MainGroup.Sport.Cardio.Solo.task7, MainGroup.Sport.Cardio.Solo.task7_help,
                        MainGroup.Sport.Cardio.Solo.task7_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Лягте на спину, уберите руки за голову и разведите локти в стороны. Поочерёдно сгибайте и выпрямляйте ноги, как будто крутите педали велосипеда, в это время локтями касайтесь колена противоположной ноги.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task7_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task7_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task7_do, MainGroup.Sport.Cardio.Solo.task7_help,
                            MainGroup.Sport.Cardio.Solo.task7) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Вы молодцы, осталось совсем немного! Начинаем отжимания.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '937455/184ba7336b4638e1442e',
                                    "title": 'Упражнение 8',
                                    "description": 'Отжимания'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task8)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state in (
                        MainGroup.Sport.Cardio.Solo.task8, MainGroup.Sport.Cardio.Solo.task8_help,
                        MainGroup.Sport.Cardio.Solo.task8_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'В планке опускаем и поднимаем тело с помощью сгибания - разгибания рук от пола.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task8_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task8_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task8_do, MainGroup.Sport.Cardio.Solo.task8_help,
                            MainGroup.Sport.Cardio.Solo.task8) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'И завершающее упражнение! Сделаем выпрыгивания из полувыпада.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '213044/ebc7322f94861b2942e9',
                                    "title": 'Упражнение 9',
                                    "description": 'Выпрыгивания из полувыпада.'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task9)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state in (
                        MainGroup.Sport.Cardio.Solo.task9, MainGroup.Sport.Cardio.Solo.task9_help,
                        MainGroup.Sport.Cardio.Solo.task9_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Выполнив небольшой шаг назад, опуститесь в полувыпад. '
                                        'Затем оттолкнитесь и в прыжке поднимите колено отведенной ноги до уровня груди. '
                                        'Вернитесь в полувыпад и повторите. Руки двигаются вдоль тела как во время бег.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task9_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task9_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Solo.task9_do, MainGroup.Sport.Cardio.Solo.task9_help,
                            MainGroup.Sport.Cardio.Solo.task9) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        answer_options = [
                            'Заминка нужна, чтобы снизить до нормального уровня частоту сердечных сокращений. Хотите её выпонить?',
                            'Будет здорово выполнить заминку! Заминка снижает склонность к закрепощению мышц после нагрузки.  Хотели бы Вы приступить к её выполнению?']
                        resp.update({
                            'response': {
                                'text': f'{random.choice(answer_options)}',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Хотите выполнить заминку?'
                                    },
                                    'items': [
                                        {"title": 'Выполнить заминку', "button": {"text": 'Да'},
                                         "image_id": '213044/9c13b9b997d78cde2579'},
                                        {"title": 'Завершить без заминки', "button": {"text": 'Нет'},
                                         "image_id": '1540737/cc47e154fc7c83b6ba0d'}

                                    ]
                                }

                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmDown.qw)
                        fsm.update_data(user_id, callback=finish_solo_cardio)

                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.end)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

                elif state == MainGroup.Sport.Cardio.Solo.end:
                    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmDown.qw)
                    fsm.update_data(user_id, callback=finish_solo_cardio)

            elif state in MainGroup.Sport.Cardio.Rope:
                if state == MainGroup.Sport.Cardio.Rope.state_1:
                    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmUp.qw)
                    fsm.update_data(user_id, callback=start_rope_cardio)
                elif state in (MainGroup.Sport.Cardio.Rope.start, MainGroup.Sport.Cardio.Rope.final):
                    if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command:
                        print(3)
                        resp.update({
                            'response': {
                                'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", "Идеальный вес",или "Фазы сна".',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Чем займёмся на этот раз? #Кнопка "идеальный вес" временно недоступна#'
                                    },
                                    'items': [
                                        {"title": 'кардиотренировка', 'button': {"text": 'кардиотренировка'},
                                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                        {"title": 'силовая тренировка', "button": {"text": 'силовая тренировка'},
                                         "description": 'описание...', "image_id": '1533899/f030bee0ec7edea516e3'},
                                        {"title": 'утренняя зарядка', "button": {"text": 'утренняя зарядка'},
                                         "description": 'описание...', "image_id": '1540737/cc26a14712e6995a6624'},
                                        {"title": 'водный баланс', "button": {"text": 'водный баланс'},
                                         "description": 'описание...', "image_id": '1540737/dc7c3c075dd3ecc22fc7'},
                                        {"title": 'фазы сна', "button": {"text": 'фазы сна'},
                                         "description": 'описание...',
                                         "image_id": '213044/e81c096eeedd03ef9a2e'}

                                    ]
                                }
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.state_home)
                    elif 'да' in command or 'готов' in command or 'повтор' in command or 'нач' in command or 'запус' in command:
                        resp.update({
                            'response': {
                                'text': 'Начинаем нашу энергичную тренировку с прыжков на скакалке.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/b7da038fa8ed18797346',
                                    "title": 'Упражнение 1',
                                    "description": 'Прыжки на скакалке'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task1)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение тренировки, или возвращаемся в меню?'
                                ,
                                'buttons': [
                                    {
                                        'title': 'Вернуться в меню',
                                        'hide': True
                                    },
                                    {
                                        'title': 'Запустить тренировку',
                                        'hide': True
                                    }
                                ]

                            }
                        })
                elif state in (
                        MainGroup.Sport.Cardio.Rope.task1, MainGroup.Sport.Cardio.Rope.task1_help,
                        MainGroup.Sport.Cardio.Rope.task1_do) or (
                        state == MainGroup.Sport.Cardio.Rope.final and 'повтор' in command):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Для выполнения этого упражнение возьмите скакалку в обе руки и начинайте вращать, одновременно перепрыгивая её.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task1_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task1_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Rope.task1_do, MainGroup.Sport.Cardio.Rope.task1_help,
                            MainGroup.Sport.Cardio.Rope.task1) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Продолжаем тренировку! Начинаем отжимания.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '997614/2fb79577b25dcbe1b8e5',
                                    "title": 'Упражнение 2',
                                    "description": 'Отжимания'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task2)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Cardio.Rope.task2, MainGroup.Sport.Cardio.Rope.task2_help,
                        MainGroup.Sport.Cardio.Rope.task2_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'В планке опускаем и поднимаем тело с помощью сгибания - разгибания рук от пола.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task2_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task2_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Rope.task2_do, MainGroup.Sport.Cardio.Rope.task2_help,
                            MainGroup.Sport.Cardio.Rope.task2) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'У Вас прекрасно получается! Продолжаем укреплять своё тело: делаем приседания с выпрыгиванием.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '937455/0f3a8ac10be8dcbc3655',
                                    "title": 'Упражнение 3',
                                    "description": 'Приседания с выпрыгиванием'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task3)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Cardio.Rope.task3, MainGroup.Sport.Cardio.Rope.task3_help,
                        MainGroup.Sport.Cardio.Rope.task3_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Поставьте ноги на ширину плеч, выпрямите спину. Можно скрестить руки перед собой на уровне груди. Присед делается на вдохе. На выдохе совершается выпрыгивание.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task3_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task3_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Rope.task3_do, MainGroup.Sport.Cardio.Rope.task3_help,
                            MainGroup.Sport.Cardio.Rope.task3) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Это было круто! А теперь знакомые прыжки на скакалке.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/b7da038fa8ed18797346',
                                    "title": 'Упражнение 4',
                                    "description": 'Прыжки на скакалке'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task4)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Cardio.Rope.task4, MainGroup.Sport.Cardio.Rope.task4_help,
                        MainGroup.Sport.Cardio.Rope.task4_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Возьмите скакалку в обе руки и начните вращать, одновременно стараясь её перепрыгнуть.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task4_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task4_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Rope.task4_do, MainGroup.Sport.Cardio.Rope.task4_help,
                            MainGroup.Sport.Cardio.Rope.task4) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Ура, завершающее упражнение! Не сбавляем темп  Далее на очереди упражнение бёрпи.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1533899/2c5cbca42380f3ebf856',
                                    "title": 'Упражнение 5',
                                    "description": 'Упражнение бёрпи'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task5)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Cardio.Rope.task5, MainGroup.Sport.Cardio.Rope.task5_help,
                        MainGroup.Sport.Cardio.Rope.task5_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Подпрыгните, отведите ноги назад и опустите таз, чтобы получилась поза планки. Соберитесь обратно прыжком, выпрямитесь, руки вытяните вверх.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task5_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_fourteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task5_do)
                    elif state in (
                            MainGroup.Sport.Cardio.Rope.task5_do, MainGroup.Sport.Cardio.Rope.task5_help,
                            MainGroup.Sport.Cardio.Rope.task5) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        answer_options = [
                            'Заминка нужна, чтобы снизить до нормального уровня частоту сердечных сокращений. Хотите её выпонить?',
                            'Будет здорово выполнить заминку! Заминка снижает склонность к закрепощению мышц после нагрузки.  Хотели бы Вы приступить к её выполнению?']
                        resp.update({
                            'response': {
                                'text': f'{random.choice(answer_options)}',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Хотите выполнить заминку?'
                                    },
                                    'items': [
                                        {"title": 'Выполнить заминку', "button": {"text": 'Да'},
                                         "image_id": '213044/9c13b9b997d78cde2579'},
                                        {"title": 'Завершить без заминки', "button": {"text": 'Нет'},
                                         "image_id": '1540737/cc47e154fc7c83b6ba0d'}

                                    ]
                                }

                            }
                        })

                        fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmDown.qw)
                        fsm.update_data(user_id, callback=finish_rope_cardio)
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.end)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state == MainGroup.Sport.Cardio.Rope.end:
                    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmDown.qw)
                    fsm.update_data(user_id, callback=finish_rope_cardio)

        elif state in MainGroup.Sport.Zaradka:
            if state == MainGroup.Sport.Zaradka.state_1:
                if 'пят' in command or '5' in command:
                    resp.update({
                        'response': {
                            'text': 'Приготовьтесь получить заряд бодрости! Каждое упражнение длится минуту.Перед выполнением каждого упражнения Вы можете изучить его подробнее, начать выполнение или пропустить его и перейти к следующему.'
                                    'Вы готовы начать или подберём другую тренировку?',
                            'card': {
                                'type': 'ItemsList',
                                'header': {
                                    'text': 'Приступаем к выполнению зарядки'
                                },
                                'items': [
                                    {"title": 'Я готов', "button": {"text": 'Я готов'},
                                     "image_id": '997614/72ab6692a3db3f4e3056'},
                                    {"title": 'Выберем другую тренировку',
                                     "button": {"text": 'Выберем другую тренировку'},
                                     "image_id": '1030494/cc3631c8499cdc8daf8b'}

                                ]
                            }

                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.start)
                elif 'дес' in command or '10' in command:
                    resp.update({
                        'response': {
                            'text': 'Итак, начинаем нашу активную 10-минутную зарядку. Надеюсь Вы полны энтузиазма. Каждое упражнение длится 60 секунд.'
                                    ' Перед выполнением каждого упражнения Вы можете изучить его подробнее, начать выполнение или пропустить его и перейти к следующему. Вы готовы начать или подберём другую тренировку?',
                            'card': {
                                'type': 'ItemsList',
                                'header': {
                                    'text': 'Приступаем к выполнению зарядки'
                                },
                                'items': [
                                    {"title": 'Я готов', "button": {"text": 'Я готов'},
                                     "image_id": '997614/72ab6692a3db3f4e3056'},
                                    {"title": 'Выберем другую тренировку',
                                     "button": {"text": 'Выберем другую тренировку'},
                                     "image_id": '1030494/cc3631c8499cdc8daf8b'}

                                ]
                            }

                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.start)
                else:
                    resp.update({
                        'response': {
                            'text': 'Уточните, пожалуйста, Вы собираетесь выполнить пятиминутную или десятиминутную тренировку?'
                            ,
                            'buttons': [
                                {
                                    'title': 'пятиминутная',
                                    'hide': True
                                },
                                {
                                    'title': 'Десятиминутная',
                                    'hide': True
                                }
                            ]

                        }
                    })
            elif state in MainGroup.Sport.Zaradka.Ten:
                if state in (MainGroup.Sport.Zaradka.Ten.start, MainGroup.Sport.Zaradka.Ten.final):
                    if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command:
                        print(4)
                        resp.update({
                            'response': {
                                'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", "Идеальный вес", или "Фазы сна".',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Чем займёмся на этот раз? #Кнопка "идеальный вес" временно недоступна#'
                                    },
                                    'items': [
                                        {"title": 'кардиотренировка', 'button': {"text": 'кардиотренировка'},
                                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                        {"title": 'силовая тренировка', "button": {"text": 'силовая тренировка'},
                                         "description": 'описание...', "image_id": '1533899/f030bee0ec7edea516e3'},
                                        {"title": 'утренняя зарядка', "button": {"text": 'утренняя зарядка'},
                                         "description": 'описание...', "image_id": '1540737/cc26a14712e6995a6624'},
                                        {"title": 'водный баланс', "button": {"text": 'водный баланс'},
                                         "description": 'описание...', "image_id": '1540737/dc7c3c075dd3ecc22fc7'},
                                        {"title": 'фазы сна', "button": {"text": 'фазы сна'},
                                         "description": 'описание...',
                                         "image_id": '213044/e81c096eeedd03ef9a2e'}

                                    ]
                                }
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.state_home)
                    elif 'да' in command or 'готов' in command or 'повтор' in command or 'нач' in command or 'запус' in command:
                        resp.update({
                            'response': {
                                'text': 'Приступаем  к растиранию шеи!',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/187806e12d9cfa5a2e7b',
                                    "title": 'Упражнение 1',
                                    "description": 'Растирание шеи'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task1)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение тренировки, или возвращаемся в меню?'
                                ,
                                'buttons': [
                                    {
                                        'title': 'Вернуться в меню',
                                        'hide': True
                                    },
                                    {
                                        'title': 'Запустить тренировку',
                                        'hide': True
                                    }
                                ]

                            }
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task1, MainGroup.Sport.Zaradka.Ten.task1_help,
                        MainGroup.Sport.Zaradka.Ten.task1_do) or (
                        state == MainGroup.Sport.Zaradka.Ten.final and 'повтор' in command):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Начинаем поглаживания тыльной стороны шеи обеими руками. Их необходимо прижимать ладонями к массируемой части. Перемещаемся от границы волосяного покрова до плечевого сустава.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task1_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task1_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task1_do, MainGroup.Sport.Zaradka.Ten.task1_help,
                            MainGroup.Sport.Zaradka.Ten.task1) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Это было легко. Постепенно усложняемся и переходим к наклонам головы.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '997614/580e288f2c7678c15fc1',
                                    "title": 'Упражнение 2',
                                    "description": 'Наклоны головы'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task2)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task2, MainGroup.Sport.Zaradka.Ten.task2_help,
                        MainGroup.Sport.Zaradka.Ten.task2_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Плавно наклоняйте голову к правому, а затем к левому плечу. Рекомендую делать упражнение как можно медленнее.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task2_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task2_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task2_do, MainGroup.Sport.Zaradka.Ten.task2_help,
                            MainGroup.Sport.Zaradka.Ten.task2) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'У Вас прекрасно получается! Разминаем кисти с помощью круговых вращений.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '213044/1e95ab71033fd2f5a670',
                                    "title": 'Упражнение 3',
                                    "description": 'круговые вращения кистей'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task3)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task3, MainGroup.Sport.Zaradka.Ten.task3_help,
                        MainGroup.Sport.Zaradka.Ten.task3_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Ладони разжаты. Удерживая плечи и предплечья неподвижными, вращение осуществляется только кистями.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task3_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task3_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task3_do, MainGroup.Sport.Zaradka.Ten.task3_help,
                            MainGroup.Sport.Zaradka.Ten.task3) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Поднажмите! Начинаем выполнять наклоны корпуса.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '965417/1f515b785dbec2f0ce30',
                                    "title": 'Упражнение 4',
                                    "description": 'Наклоны корпуса'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task4)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task4, MainGroup.Sport.Zaradka.Ten.task4_help,
                        MainGroup.Sport.Zaradka.Ten.task4_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Не отрывая ног от пола, начинаем наклонять тело в правую, а затем в левую сторону, руки лучше держать на поясе.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task4_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task4_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task4_do, MainGroup.Sport.Zaradka.Ten.task4_help,
                            MainGroup.Sport.Zaradka.Ten.task4) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Теперь снова простое упражнение - вращение рук.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '997614/ad34ebeedaa748ebfb6b',
                                    "title": 'Упражнение 5',
                                    "description": 'Вращение рук'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task5)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task5, MainGroup.Sport.Zaradka.Ten.task5_help,
                        MainGroup.Sport.Zaradka.Ten.task5_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Встаньте прямо и вытяните руки по сторонам. Тело образует букву «Т». Это исходное положение. Выполняйте круговые движения прямыми руками вперёд, затем – назад.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task5_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task5_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task5_do, MainGroup.Sport.Zaradka.Ten.task5_help,
                            MainGroup.Sport.Zaradka.Ten.task5) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'На очереди весёлое упражнение - круговые вращения тазом.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '213044/6aeb0022c72fb9c0256f',
                                    "title": 'Упражнение 6',
                                    "description": 'круговые вращения тазом'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task6)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task6, MainGroup.Sport.Zaradka.Ten.task6_help,
                        MainGroup.Sport.Zaradka.Ten.task6_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Положите руки на талию, ноги расставьте шире плеч. Начните вращать тазом по кругу, как будто стараетесь нарисовать круг ягодицами. Стопы не отрываются от пола, вращение происходит за счет движений таза, а не корпуса.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task6_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task6_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task6_do, MainGroup.Sport.Zaradka.Ten.task6_help,
                            MainGroup.Sport.Zaradka.Ten.task6) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Вы молодцы, осталось совсем немного! Начинаем отжимания. ',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1652229/36613a381d93ed552a89',
                                    "title": 'Упражнение 7',
                                    "description": 'Отжимания'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task7)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task7, MainGroup.Sport.Zaradka.Ten.task7_help,
                        MainGroup.Sport.Zaradka.Ten.task7_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'В планке опускаем и поднимаем тело с помощью сгибания - разгибания рук от пола.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task7_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task7_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task7_do, MainGroup.Sport.Zaradka.Ten.task7_help,
                            MainGroup.Sport.Zaradka.Ten.task7) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'А теперь выполняем бег на месте.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '965417/8252b9ad0168a76edcfb',
                                    "title": 'Упражнение 8',
                                    "description": 'Бег на месте'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task8)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task8, MainGroup.Sport.Zaradka.Ten.task8_help,
                        MainGroup.Sport.Zaradka.Ten.task8_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'По сути это тот же бег, но без передвижения. Спину необходимо держать прямо и ровно; руки согнуть в локтях, не задирая и не расслабляя их слишком сильно',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task8_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task8_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task8_do, MainGroup.Sport.Zaradka.Ten.task8_help,
                            MainGroup.Sport.Zaradka.Ten.task8) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Вы, настоящий спортсмен! Далее переходим к наклонам корпуса. ',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '965417/49420910ad42b27d16ed',
                                    "title": 'Упражнение 9',
                                    "description": 'Наклоны корпуса'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task9)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task9, MainGroup.Sport.Zaradka.Ten.task9_help,
                        MainGroup.Sport.Zaradka.Ten.task9_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Ноги на ширине плеч, спина прямая, лопатки сведены, руки подняты к ушам. Напрягите пресс и наклоняйтесь вниз. Постарайтесь тянуться грудью к бедрам, а не руками к полу.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task9_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task9_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task9_do, MainGroup.Sport.Zaradka.Ten.task9_help,
                            MainGroup.Sport.Zaradka.Ten.task9) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Поднажмём, последнее упражнение - это упражнение на пресс, а точнее поднятие корпуса лёжа на спине. ',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '997614/d843aa7bd19d82dfddbc',
                                    "title": 'Упражнение 10',
                                    "description": 'Поднятие корпуса лёжа на спине'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task10)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task10, MainGroup.Sport.Zaradka.Ten.task10_help,
                        MainGroup.Sport.Zaradka.Ten.task10_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Ложимся на спину, прижимаем поясницу к полу, ноги чуть сгибаем в коленях. Руки закрепляем за головой или на груди. Локти разводим в стороны.'
                                        'Начинаем сгибание туловища. Подбородком тянемся к груди. Тянемся дальше, чтобы вслед за головой и шеей от пола отрывалась спина.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task10_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.task10_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task10_do, MainGroup.Sport.Zaradka.Ten.task10_help,
                            MainGroup.Sport.Zaradka.Ten.task10) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Вы хорошо потрудились, поздравляю вас с очередной победой! Что вы выберите дальше: повторить или завершить тренировку?',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Повторим тренировку или вернёмся в меню?'
                                    },
                                    'items': [
                                        {"title": 'Повторить тренировку', "button": {"text": 'Повторить тренировку'},
                                         "image_id": '997614/15f977696a281092bcc0'},
                                        {"title": 'Вернуться в меню',
                                         "button": {"text": 'Вернуться в меню'},
                                         "image_id": '1030494/cc3631c8499cdc8daf8b'}

                                    ]
                                }

                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Ten.final)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

            elif state in MainGroup.Sport.Zaradka.Five:
                if state in (MainGroup.Sport.Zaradka.Five.start, MainGroup.Sport.Zaradka.Five.final):
                    if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command:
                        print(5)
                        resp.update({
                            'response': {
                                'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", "Идеальный вес", или "Фазы сна".',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Чем займёмся на этот раз? #Кнопка "идеальный вес" временно недоступна#'
                                    },
                                    'items': [
                                        {"title": 'кардиотренировка', 'button': {"text": 'кардиотренировка'},
                                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                        {"title": 'силовая тренировка', "button": {"text": 'силовая тренировка'},
                                         "description": 'описание...', "image_id": '1533899/f030bee0ec7edea516e3'},
                                        {"title": 'утренняя зарядка', "button": {"text": 'утренняя зарядка'},
                                         "description": 'описание...', "image_id": '1540737/cc26a14712e6995a6624'},
                                        {"title": 'водный баланс', "button": {"text": 'водный баланс'},
                                         "description": 'описание...', "image_id": '1540737/dc7c3c075dd3ecc22fc7'},
                                        {"title": 'фазы сна', "button": {"text": 'фазы сна'},
                                         "description": 'описание...',
                                         "image_id": '213044/e81c096eeedd03ef9a2e'}

                                    ]
                                }
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.state_home)
                    elif 'да' in command or 'готов' in command or 'повтор' in command or 'нач' in command or 'запус' in command:
                        resp.update({
                            'response': {
                                'text': 'Открывают нашу тренировку наклоны головы.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1652229/ee34512c3b9684ab74b7',
                                    "title": 'Упражнение 1',
                                    "description": 'Наклоны головы'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task1)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение тренировки, или возвращаемся в меню?'
                                ,
                                'buttons': [
                                    {
                                        'title': 'Вернуться в меню',
                                        'hide': True
                                    },
                                    {
                                        'title': 'Запустить тренировку',
                                        'hide': True
                                    }
                                ]

                            }
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Five.task1, MainGroup.Sport.Zaradka.Five.task1_help,
                        MainGroup.Sport.Zaradka.Five.task1_do) or (
                        state == MainGroup.Sport.Zaradka.Five.final and 'повтор' in command):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Руки на поясе, ноги на ширине плеч, грудная клетка расправлена, живот втянут. Наклоны головы по очереди к правому и левому плечу',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task1_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task1_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Five.task1_do, MainGroup.Sport.Zaradka.Five.task1_help,
                            MainGroup.Sport.Zaradka.Five.task1) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Далее разминаем руки круговыми вращениями.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1521359/be1b4290513642ff2e69',
                                    "title": 'Упражнение 2',
                                    "description": 'Круговые движения рук'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task2)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Five.task2, MainGroup.Sport.Zaradka.Five.task2_help,
                        MainGroup.Sport.Zaradka.Five.task2_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': ' Ладони должны быть разжаты. Удерживая плечи и предплечья неподвижными, вращайте кистями.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task2_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task2_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Five.task2_do, MainGroup.Sport.Zaradka.Five.task2_help,
                            MainGroup.Sport.Zaradka.Five.task2) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'А теперь перейдём к полным круговым вращениям.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/207c36753da8da2dd64d',
                                    "title": 'Упражнение 3',
                                    "description": 'Полные круговые вращения'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task3)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Five.task3, MainGroup.Sport.Zaradka.Five.task3_help,
                        MainGroup.Sport.Zaradka.Five.task3_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Встаньте прямо и вытяните руки по сторонам. Тело образует букву «Т». Выполняйте круговые движения прямыми руками вперёд, затем – назад.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task3_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task3_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Five.task3_do, MainGroup.Sport.Zaradka.Five.task3_help,
                            MainGroup.Sport.Zaradka.Five.task3) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Наращиваем интенсивность. Не беспокойтесь, делаем классические приседания.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/8c6ed8b8b2ea3d6c636d',
                                    "title": 'Упражнение 4',
                                    "description": 'Приседания'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task4)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Five.task4, MainGroup.Sport.Zaradka.Five.task4_help,
                        MainGroup.Sport.Zaradka.Five.task4_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Чтобы выполнить стандартное приседание, нужно держать спину прямо. После чего начните медленно опускать бедра, пока они не станут параллельны полу. ',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task4_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task4_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Five.task4_do, MainGroup.Sport.Zaradka.Five.task4_help,
                            MainGroup.Sport.Zaradka.Five.task4) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Ого, у вас хорошо получается, разнообразим тренировку необычным бегом на месте.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1030494/a858ba400c31046a469f',
                                    "title": 'Упражнение 5',
                                    "description": 'Бег на месте'
                                }
                                ,
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task5)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })
                elif state in (
                        MainGroup.Sport.Zaradka.Five.task5, MainGroup.Sport.Zaradka.Five.task5_help,
                        MainGroup.Sport.Zaradka.Five.task5_do):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'По сути это тот же бег, но без передвижения. Спину необходимо держать прямо и ровно; руки согнуть в локтях. Важно не задирать и не расслаблять их слишком сильно.',
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
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task5_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(motivations)}',
                                'tts': f'{random.choice(tracks_sixteen)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task5_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Five.task5_do, MainGroup.Sport.Zaradka.Five.task5_help,
                            MainGroup.Sport.Zaradka.Five.task5) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Вы хорошо потрудились, горжусь Вами. Что делаем дальше: повторим или завершим тренировку? Выбор за Вами.',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Повторим тренировку или вернёмся в меню?'
                                    },
                                    'items': [
                                        {"title": 'Повторить тренировку', "button": {"text": 'Повторить тренировку'},
                                         "image_id": '997614/15f977696a281092bcc0'},
                                        {"title": 'Вернуться в меню',
                                         "button": {"text": 'Вернуться в меню'},
                                         "image_id": '1030494/cc3631c8499cdc8daf8b'}

                                    ]
                                }

                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.final)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                                ,
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
                        })

        elif state in MainGroup.Sport.Power:
            if state in (MainGroup.Sport.Power.start, MainGroup.Sport.Power.final):
                if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command:
                    print(6)
                    resp.update({
                        'response': {
                            'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", или "Идеальный вес", "Фазы сна".',
                            'card': {
                                'type': 'ItemsList',
                                'header': {
                                    'text': 'Чем займёмся на этот раз? #Кнопка "идеальный вес" временно недоступна#'
                                },
                                'items': [
                                    {"title": 'кардиотренировка', 'button': {"text": 'кардиотренировка'},
                                     "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                    {"title": 'силовая тренировка', "button": {"text": 'силовая тренировка'},
                                     "description": 'описание...', "image_id": '1533899/f030bee0ec7edea516e3'},
                                    {"title": 'утренняя зарядка', "button": {"text": 'утренняя зарядка'},
                                     "description": 'описание...', "image_id": '1540737/cc26a14712e6995a6624'},
                                    {"title": 'водный баланс', "button": {"text": 'водный баланс'},
                                     "description": 'описание...', "image_id": '1540737/dc7c3c075dd3ecc22fc7'},
                                    {"title": 'фазы сна', "button": {"text": 'фазы сна'},
                                     "description": 'описание...',
                                     "image_id": '213044/e81c096eeedd03ef9a2e'}

                                ]
                            }
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.state_home)
                elif 'да' in command or 'готов' in command or 'повтор' in command or 'нач' in command or 'запус' in command:
                    resp.update({
                        'response': {
                            'text': 'Давайте начнем. Первое упражнение - отжимания. ',
                            'card': {
                                'type': 'BigImage',
                                "image_id": '937455/184ba7336b4638e1442e',
                                "title": 'Упражнение 1',
                                "description": 'Отжимания'
                            }
                            ,
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task1)
                else:
                    resp.update({
                        'response': {
                            'text': 'Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение тренировки, или возвращаемся в меню?'
                            ,
                            'buttons': [
                                {
                                    'title': 'Вернуться в меню',
                                    'hide': True
                                },
                                {
                                    'title': 'Запустить тренировку',
                                    'hide': True
                                }
                            ]

                        }
                    })
            elif state in (
                    MainGroup.Sport.Power.task1, MainGroup.Sport.Power.task1_help, MainGroup.Sport.Power.task1_do) or (
                    state == MainGroup.Sport.Power.final and 'повтор' in command):
                if 'подробн' in command or 'объяс' in command:
                    resp.update({
                        'response': {
                            'text': 'Примите упор лежа и начинайте выполнять сгибания и разгибания рук. Следите за тем, чтобы линия вашего корпуса оставалась прямой, избегайте прогибов в области груди и поясницы.',
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task1_help)
                elif 'выполн' in command or 'дел' in command:
                    resp.update({
                        'response': {
                            'text': f'{random.choice(motivations)}',
                            'tts': f'{random.choice(tracks_fourteen)}',
                            'buttons': [
                                {
                                    'title': 'Следующее упражнение▶',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task1_do)
                elif state in (
                        MainGroup.Sport.Power.task1_do, MainGroup.Sport.Power.task1_help,
                        MainGroup.Sport.Power.task1) and (
                        'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                    resp.update({
                        'response': {
                            'text': 'У Вас здорово получается! Следующее упражнение - подтягивания.',
                            'card': {
                                'type': 'BigImage',
                                "image_id": '213044/18bfa946ccc5da2c8e45',
                                "title": 'Упражнение 2',
                                "description": 'Подтягивания'
                            }
                            ,
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task2)
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                            ,
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
                    })
            elif state in (
                    MainGroup.Sport.Power.task2, MainGroup.Sport.Power.task2_help, MainGroup.Sport.Power.task2_do) or (
                    state == MainGroup.Sport.Power.final and 'повтор' in command):
                if 'подробн' in command or 'объяс' in command:
                    resp.update({
                        'response': {
                            'text': 'Повисните на турнике и сделайте тяговое движение вверх, одновременно с этим делая выдох. Движение должно осуществляться за счет движения лопаток.'
                                    ' Не надо стараться тянуть себя вверх силой бицепсов, так как широчайшие мышцы спины – куда более сильная мышечная группа.',
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task2_help)
                elif 'выполн' in command or 'дел' in command:
                    resp.update({
                        'response': {
                            'text': f'{random.choice(motivations)}',
                            'tts': f'{random.choice(tracks_fourteen)}',
                            'buttons': [
                                {
                                    'title': 'Следующее упражнение▶',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task2_do)
                elif state in (
                        MainGroup.Sport.Power.task2_do, MainGroup.Sport.Power.task2_help,
                        MainGroup.Sport.Power.task2) and (
                        'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                    resp.update({
                        'response': {
                            'text': 'Надеюсь Вы готовы, потому что мы начинаем наращивать интенсивность. Приступаем к отжиманиям обратным хватом.',
                            'card': {
                                'type': 'BigImage',
                                "image_id": '213044/e3204402f44ed1603aeb',
                                "title": 'Упражнение 3',
                                "description": 'Отжимания обратным хватом'
                            }
                            ,
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task3)
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                            ,
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
                    })
            elif state in (
                    MainGroup.Sport.Power.task3, MainGroup.Sport.Power.task3_help, MainGroup.Sport.Power.task3_do) or (
                    state == MainGroup.Sport.Power.final and 'повтор' in command):
                if 'подробн' in command or 'объяс' in command:
                    resp.update({
                        'response': {
                            'text': 'Садимся на возвышенность (можно использовать стул), упираемся ладонями так, чтобы руки были на одинаковом расстоянии от линии позвоночника. '
                                    'Сгибаем руки в локтевых и плечевых суставах одновременно, опускаемся тазом вниз до уровня, когда предплечья станут параллельными полу. С выдохом разгибаем руки.',
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task3_help)
                elif 'выполн' in command or 'дел' in command:
                    resp.update({
                        'response': {
                            'text': f'{random.choice(motivations)}',
                            'tts': f'{random.choice(tracks_fourteen)}',
                            'buttons': [
                                {
                                    'title': 'Следующее упражнение▶',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task3_do)
                elif state in (
                        MainGroup.Sport.Power.task3_do, MainGroup.Sport.Power.task3_help,
                        MainGroup.Sport.Power.task3) and (
                        'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                    resp.update({
                        'response': {
                            'text': 'Вы - настоящий спортсмен! Приступаем к приседаниям.',
                            'card': {
                                'type': 'BigImage',
                                "image_id": '1656841/46115bb0d16cbb24a76b',
                                "title": 'Упражнение 4',
                                "description": 'Приседания'
                            }
                            ,
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task4)
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                            ,
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
                    })
            elif state in (
                    MainGroup.Sport.Power.task4, MainGroup.Sport.Power.task4_help, MainGroup.Sport.Power.task4_do) or (
                    state == MainGroup.Sport.Power.final and 'повтор' in command):
                if 'подробн' in command or 'объяс' in command:
                    resp.update({
                        'response': {
                            'text': 'Встаньте прямо, ноги на ширине плеч, носки стоп слега разведите в стороны. Напрягите поясницу, '
                                    'отведите таз назад и немного наклоните торс вперед, согните ноги в коленях и опуститесь как можно ниже. Затем поднимитесь в исходное положение.',
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task4_help)
                elif 'выполн' in command or 'дел' in command:
                    resp.update({
                        'response': {
                            'text': f'{random.choice(motivations)}',
                            'tts': f'{random.choice(tracks_fourteen)}',
                            'buttons': [
                                {
                                    'title': 'Следующее упражнение▶',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task4_do)
                elif state in (
                        MainGroup.Sport.Power.task4_do, MainGroup.Sport.Power.task4_help,
                        MainGroup.Sport.Power.task4) and (
                        'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                    resp.update({
                        'response': {
                            'text': 'Поднажмите, осталось не так много! Следующее упражнение - поднимания на носке.',
                            'card': {
                                'type': 'BigImage',
                                "image_id": '1030494/ac5faee74949ee038bad',
                                "title": 'Упражнение 5',
                                "description": 'Поднимания на носке'
                            }
                            ,
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task5)
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                            ,
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
                    })
            elif state in (
                    MainGroup.Sport.Power.task5, MainGroup.Sport.Power.task5_help, MainGroup.Sport.Power.task5_do) or (
                    state == MainGroup.Sport.Power.final and 'повтор' in command):
                if 'подробн' in command or 'объяс' in command:
                    resp.update({
                        'response': {
                            'text': 'Встаньте прямо и начинайте подниматься на носки и вновь опускаться на всю стопу. Вы можете воспользоваться дополнительной опорой, например, стенкой, если Вам это необходимо.',
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task5_help)
                elif 'выполн' in command or 'дел' in command:
                    resp.update({
                        'response': {
                            'text': f'{random.choice(motivations)}',
                            'tts': f'{random.choice(tracks_fourteen)}',
                            'buttons': [
                                {
                                    'title': 'Следующее упражнение▶',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task5_do)
                elif state in (
                        MainGroup.Sport.Power.task5_do, MainGroup.Sport.Power.task5_help,
                        MainGroup.Sport.Power.task5) and (
                        'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                    resp.update({
                        'response': {
                            'text': 'Следующее энергичное упражнение - велосипед.',
                            'card': {
                                'type': 'BigImage',
                                "image_id": '997614/1ef3a8d9152694fe40e3',
                                "title": 'Упражнение 6',
                                "description": 'Велосипед'
                            }
                            ,
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task6)
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                            ,
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
                    })
            elif state in (
                    MainGroup.Sport.Power.task6, MainGroup.Sport.Power.task6_help, MainGroup.Sport.Power.task6_do) or (
                    state == MainGroup.Sport.Power.final and 'повтор' in command):
                if 'подробн' in command or 'объяс' in command:
                    resp.update({
                        'response': {
                            'text': 'Лягте на спину, уберите руки за голову и разведите локти в стороны. Поочерёдно сгибайте и выпрямляйте ноги, '
                                    'как будто крутите педали велосипеда, в это время локтями касайтесь колена противоположной ноги.',
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task6_help)
                elif 'выполн' in command or 'дел' in command:
                    resp.update({
                        'response': {
                            'text': f'{random.choice(motivations)}',
                            'tts': f'{random.choice(tracks_fourteen)}',
                            'buttons': [
                                {
                                    'title': 'Следующее упражнение▶',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task6_do)
                elif state in (
                        MainGroup.Sport.Power.task6_do, MainGroup.Sport.Power.task6_help,
                        MainGroup.Sport.Power.task6) and (
                        'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                    resp.update({
                        'response': {
                            'text': 'Выходим на финишную прямую! Завершающее упражнение - сгибанию рук с грузом.',
                            'card': {
                                'type': 'BigImage',
                                "image_id": '213044/a225c7950958cf314e50',
                                "title": 'Упражнение 7',
                                "description": 'Сгибание рук с грузом'
                            }
                            ,
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task7)
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                            ,
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
                    })
            elif state in (
                    MainGroup.Sport.Power.task7, MainGroup.Sport.Power.task7_help, MainGroup.Sport.Power.task7_do) or (
                    state == MainGroup.Sport.Power.final and 'повтор' in command):
                if 'подробн' in command or 'объяс' in command:
                    resp.update({
                        'response': {
                            'text': 'Примите удобное положение. Возьмите любой груз, удобно лежащий в руке, и начинайте сгибание руки.',
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task7_help)
                elif 'выполн' in command or 'дел' in command:
                    resp.update({
                        'response': {
                            'text': f'{random.choice(motivations)}',
                            'tts': f'{random.choice(tracks_fourteen)}',
                            'buttons': [
                                {
                                    'title': 'Следующее упражнение▶',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task7_do)
                elif state in (
                        MainGroup.Sport.Power.task7_do, MainGroup.Sport.Power.task7_help,
                        MainGroup.Sport.Power.task7) and (
                        'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                    resp.update({
                        'response': {
                            'text': 'Отлично, Вы здорово справились со всеми заданиями. Отдохните и переведите дух. ',
                            'card': {
                                'type': 'BigImage',
                                "image_id": '997614/d843aa7bd19d82dfddbc',
                                "title": 'Отдых',
                                "description": 'Отдохните и переведите дух. '
                            }
                            ,
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task8)
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                            ,
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
                    })
            elif state in (
                    MainGroup.Sport.Power.task8, MainGroup.Sport.Power.task8_help, MainGroup.Sport.Power.task8_do) or (
                    state == MainGroup.Sport.Power.final and 'повтор' in command):
                if 'подробн' in command or 'объяс' in command:
                    resp.update({
                        'response': {
                            'text': 'Просто отдохните. В этом нет ничего сложного😁',
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
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task8_help)
                elif 'выполн' in command or 'дел' in command:
                    resp.update({
                        'response': {
                            'text': f'{random.choice(motivations)}',
                            'tts': f'{random.choice(tracks_fourteen)}',
                            'buttons': [
                                {
                                    'title': 'Следующее упражнение▶',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Power.task8_do)
                elif (state in (
                        MainGroup.Sport.Power.task8_do, MainGroup.Sport.Power.task8_help,
                        MainGroup.Sport.Power.task8) and (
                              'проп' in command or 'след' in command or 'прод' in command or 'дал' in command)) or \
                        state == MainGroup.Sport.Power.end:
                    answer_options = [
                        'Заминка нужна, чтобы снизить до нормального уровня частоту сердечных сокращений. Хотите её выпонить?',
                        'Будет здорово выполнить заминку! Заминка снижает склонность к закрепощению мышц после нагрузки.  Хотели бы Вы приступить к её выполнению?']
                    resp.update({
                        'response': {
                            'text': f'{random.choice(answer_options)}',
                            'card': {
                                'type': 'ItemsList',
                                'header': {
                                    'text': 'Хотите выполнить заминку?'
                                },
                                'items': [
                                    {"title": 'Выполнить заминку', "button": {"text": 'Да'},
                                     "image_id": '213044/9c13b9b997d78cde2579'},
                                    {"title": 'Завершить без заминки', "button": {"text": 'Нет'},
                                     "image_id": '1540737/cc47e154fc7c83b6ba0d'}

                                ]
                            }

                        }
                    })
                    fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmDown.qw)
                    fsm.update_data(user_id, callback=finish_power_training)
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"'
                            ,
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
                    })
            elif state == MainGroup.Sport.Power.final:
                answer_options = [
                    'Давайте выполним заминку! Она нужна, чтобы нормализовать частоту сердечных сокращений и температуру тела. Хотите снять мышечное напряжение после тренировки?',
                    'Будет здорово выполнить заминку! Она помогает снизить синдром отсроченного начала мышечной болезненности. Хотите выполнить этот ряд упражнений?']
                resp.update({
                    'response': {
                        'text': f'{random.choice(answer_options)}',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': 'Хотите выполнить заминку?'
                            },
                            'items': [
                                {"title": 'Выполнить заминку', "button": {"text": 'Да'},
                                 "image_id": '213044/9c13b9b997d78cde2579'},
                                {"title": 'Завершить без заминки', "button": {"text": 'Нет'},
                                 "image_id": '1540737/cc47e154fc7c83b6ba0d'}

                            ]
                        }

                    }
                })

                fsm.set_state(user_id, MainGroup.Sport.Power.end)

        elif state in MainGroup.Sport.Wrap.WarmUp:
            step: TrainingStep = warm_up_algorithm[fsm.get_data(user_id).get('step', 0)]

            if state == MainGroup.Sport.Wrap.WarmUp.qw:
                if 'нет' in command or 'не ' in command:
                    resp = cancel_warmup(user_id, resp)
                elif 'да' in command or 'конечн' in command:
                    resp = start_warmup(user_id, resp)
                else:
                    resp.update({
                        'response': {
                            'text': 'Извините, кажется я прослушала😣\nВы хотите выполнить разминку?'
                            ,
                            'buttons': [
                                {
                                    'title': 'Да',
                                    'hide': True
                                },
                                {
                                    'title': 'Нет',
                                    'hide': True
                                }
                            ]

                        }
                    })

            elif state == MainGroup.Sport.Wrap.WarmUp.start and is_positive(command):
                fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmUp.task)
                step: int = 0
                fsm.update_data(user_id, step=step)

                step: TrainingStep = warm_up_algorithm[step]

                resp.update(step.generate_choice_resp())

            elif 'подробн' in command or 'расскажи' in command:
                resp.update(step.generate_detailed_description_resp())

            elif is_positive(command):
                resp.update(step.generate_do_training_resp(random.choice(motivations), random.choice(tracks_fourteen)))

            elif state == MainGroup.Sport.Wrap.WarmUp.end:
                if 'повтор' in command or 'ещё' in command or 'еще' in command or 'снов' in command:
                    resp = start_warmup(user_id, resp)
                else:
                    print('cancel')
                    cancel_warmup(user_id, resp)

            elif 'пропуст' in command or 'следующ' in command or 'дальш' in command or 'продолж' in command:
                if state == MainGroup.Sport.Wrap.WarmUp.task:
                    step = fsm.get_data(user_id).get('step', 0) + 1
                    fsm.update_data(user_id, step=step)
                    print(f'{step=}')

                    try:
                        step: TrainingStep = warm_up_algorithm[step]
                    except IndexError:
                        end_warmup(user_id, resp)
                    else:
                        resp.update(step.generate_choice_resp())

                elif state == MainGroup.Sport.Wrap.WarmUp.start:
                    cancel_warmup(user_id, resp)

            else:
                end_warmup(user_id, resp)

        elif state in MainGroup.Sport.Wrap.WarmDown:
            step: TrainingStep = warm_down_algorithm[fsm.get_data(user_id).get('step', 0)]

            if state == MainGroup.Sport.Wrap.WarmDown.qw:
                if 'нет' in command or 'не ' in command:
                    resp = cancel_warmdown(user_id, resp)
                elif 'да' in command or 'конечн' in command:
                    resp = start_warmdown(user_id, resp)
                else:
                    resp.update({
                        'response': {
                            'text': 'Извините, кажется я прослушала😣\nВы хотите выполнить разминку?'
                            ,
                            'buttons': [
                                {
                                    'title': 'Да',
                                    'hide': True
                                },
                                {
                                    'title': 'Нет',
                                    'hide': True
                                }
                            ]

                        }
                    })

            elif state == MainGroup.Sport.Wrap.WarmDown.start and is_positive(command):
                fsm.set_state(user_id, MainGroup.Sport.Wrap.WarmDown.task)
                step: int = 0
                fsm.update_data(user_id, step=step)

                step: TrainingStep = warm_down_algorithm[step]

                resp.update(step.generate_choice_resp())

            elif 'подробн' in command or 'расскажи' in command:
                resp.update(step.generate_detailed_description_resp())

            elif is_positive(command):
                resp.update(step.generate_do_training_resp(random.choice(motivations), random.choice(tracks_fourteen)))

            elif state == MainGroup.Sport.Wrap.WarmDown.end:
                if 'повтор' in command or 'ещё' in command or 'еще' in command or 'снов' in command:
                    resp = start_warmdown(user_id, resp)
                else:
                    print('cancel')
                    cancel_warmdown(user_id, resp)

            elif 'пропуст' in command or 'следующ' in command or 'дальш' in command or 'продолж' in command:
                if state == MainGroup.Sport.Wrap.WarmDown.task:
                    step = fsm.get_data(user_id).get('step', 0) + 1
                    fsm.update_data(user_id, step=step)
                    print(f'{step=}')

                    try:
                        step: TrainingStep = warm_down_algorithm[step]
                    except IndexError:
                        end_warmdown(user_id, resp)
                    else:
                        resp.update(step.generate_choice_resp())

                elif state == MainGroup.Sport.Wrap.WarmDown.start:
                    cancel_warmdown(user_id, resp)

            else:
                end_warmdown(user_id, resp)

    else:
        resp.update({
            'response': {
                'text': f'Произошла ошибка. Скажите "поехали" чтобы вернуться в главное меню.'
            }
        })
        fsm.set_state(user_id, MainGroup.state_1)

    if not (response := resp.get('response', {'text': 'Затычечный текст на случай если сообщение не захендлилось'})):
        resp['response'] = response
    if not (buttons := response.get('buttons', [])):
        response['buttons'] = buttons

    for button in buttons:
        if button.get('title', '').lower() == 'помощь':
            break
    else:
        buttons.append({'title': 'Помощь', 'hide': False})
    fsm.update_data(user_id, last_buttons=buttons)

    return dict_to_json(resp, ensure_ascii=False, indent=2)


app.run('localhost', port=5050, debug=True)
