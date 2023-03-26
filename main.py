import json
import random

from flask import Flask, request

from typing_ import FriendlyDict, AliceUserRequest
from fsm import StatesGroup, State, FSM
from time_parsing import parse_time, iter_go_sleep_time

app = Flask(__name__)

fsm = FSM()


def dict_to_json(dict_: dict, *args, **kwargs):
    for key, value in dict_.items():
        if isinstance(value, FriendlyDict):
            dict_[key] = value.to_dict()
    return json.dumps(dict_, *args, **kwargs)


class MainGroup(StatesGroup):  # Состояние по умолчанию это None, его не нужно явно определять
    _fsm = fsm
    _default_state = None

    state_1 = State()

    class Water(StatesGroup):
        state_1 = State()
        end = State()

    class Dream(StatesGroup):
        state_1 = State()
        end = State()

        class Dream(StatesGroup):
            state_1 = State()
            end = State()

    class Sport(StatesGroup):
        class Wrap(StatesGroup):
            class WarmUp(StatesGroup):
                inp_state = State()
                do_task = State()

        state_home = State()

        class Power(StatesGroup):
            state_1 = State()

        class Cardio(StatesGroup):
            state_1 = State()

            class Solo(StatesGroup):
                state_1 = State()
                start = State()
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
                end = State()
                final = State()

            class Rope(StatesGroup):
                state_1 = State()
                start = State()
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
                final = State()

        class Zaradka(StatesGroup):
            state_1 = State()
            start = State()
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
            task10 = State()
            task10_help = State()
            task10_do = State()
            end = State()
            final = State()

            class Five(StatesGroup):
                start = State()
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
                end = State()
                final = State()

            class Ten(StatesGroup):
                start = State()

# Шаблон для условий:  if fsm.get_state(user_id) == MyStates.state_1
# Диаграмма: https://miro.com/app/board/uXjVMdrXZW0=/

@app.route('/alice', methods=['POST'])
def main():
    req = AliceUserRequest(request.data.decode())
    motivation = ['Удачи!', 'Так держать!', 'Вы справитесь!']
    command = req.request.command
    user_id = req.session.user.user_id
    res = {'version': req.version,
           'session': req.session}

    print(fsm.get_state(user_id))
    if req.session.new:
        # Действия при новой сессии
        answer_options = ['Привет🖐!  Всегда хотели окунуться в мир здорового образа жизни? '
                          'Поздравляю, Вы сделали правильный выбор.'
                          'Я навык ... помогу освоить основы ЗОЖ на практике с лёгкостью и удовольствием.'
                          'Если хотите ознакомиться с моим функционалом, то скажите "Что ты умеешь?". Если же готовы приступить, то скажите "Поехали".',

                          'Очень приятно осознавать, что Вы решили заботится о себе и своём здоровье💖!'
                          ' Я позабочусь о Вас и облегчу ваше знакомство с ЗОЖ. Вы сможете начать следить за Вашим здоровьем с удовольствием.'
                          ' Если нужно ознакомиться с функционалом навыка, то скажите "Что ты умеешь?". Если уже хотите приступить, то скажите "Поехали".']
        res.update({
            'response': {
                'text': f'{random.choice(answer_options)}',
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
        fsm.reset_state(user_id)
        return dict_to_json(res, ensure_ascii=False, indent=2)

    # res = []  # TODO: Заменить на сообщение об ошибке
    if fsm.get_state(user_id) is None and (command == 'что ты умеешь'):
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

        res.update({
            'response': {
                'text': f'{random.choice(answer_options)} \n',
                "tts": "<speaker audio=\"dialogs-upload/063cdddd-d9f0-40a7-9fa8-ff5ab745aa44/6c3fc433-846b-4971-91f0-77b3a9f405bb.opus\">",
                'buttons': [
                    {
                        'title': 'Поехали!',
                        'hide': True
                    }
                ]

            }
        })
        fsm.set_state(user_id, MainGroup.state_1)
        return dict_to_json(res, ensure_ascii=False, indent=2)

    elif (fsm.get_state(user_id) in (MainGroup.state_1, None)) and (
            'поехали' in command or 'нач' in command):  # TODO: Добавить в условия номера стейтов, из которых можно сюда попасть (см. диаграмму)
        # answer_options = ['Вау, Вы уже в нескольких шагах от здорового образа жизни очень рада за Вас 😍. '
        #                   'Для начала выберите, чем хотите заняться или что Вам нужно узнать:'
        #                   ' "Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".',
        #
        #                   'Вы уже совсем-совсем близко к здоровой жизни 😍, горжусь Вами. '
        #                   'Время выбирать, чем хотите заняться или что Вам нужно узнать:\n'
        #                   '"Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".']

        res.update({
            'response': {
                'text': 'XXXTentation is alive',
                'tts': f'Вы уже в нескольких шагах от здорового образа жизни! Чем сегодня займёмся? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", или "Фазы сна".',
                'card': {
                    'type': 'ItemsList',
                    'header': {
                        'text': 'Чем сегодня займёмся? Выбирайте:'
                    },
                    'items': [
                        {"title": 'кардиотреннировка', 'button': {"text": 'кардиотреннировка'},
                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                        {"title": 'силовая треннировка', "button": {"text": 'силовая треннировка'},
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
        fsm.set_state(user_id, MainGroup.Sport.state_home)

    elif fsm.get_state(user_id) in MainGroup.Sport:
        if 'вернуться' in command or 'назад' in command or 'основ' in command or 'домой' in command or 'начало' in command:
            res.update({
                'response': {
                    'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", или "Фазы сна".',
                    'card': {
                        'type': 'ItemsList',
                        'header': {
                            'text': 'Чем займёмся на этот раз?'
                        },
                        'items': [
                            {"title": 'кардиотреннировка', 'button': {"text": 'кардиотреннировка'},
                             "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                            {"title": 'силовая треннировка', "button": {"text": 'силовая треннировка'},
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
        elif fsm.get_state(user_id) == MainGroup.Sport.state_home:
            if 'вод' in command or 'баланс' in command:
                answer_options = [
                    'Вода жизненно необходима каждому человеку, а употребление её дневной нормы улучшает метаболизм. Я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. Подскажите, пожалуйста, Ваш вес.',

                    'Так как мы состоим из воды примерно на 70% 🐳, то употреблять её в достаточном количестве очень важно. '
                    'Не переживайте 😉 , я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. '
                    'Для того, чтобы точно рассчитать минимальное объём воды, мне нужен вес человека. Подскажите, пожалуйста, вес Вашего тела в килограммах.']

                res.update({
                    'response': {
                        'text': f'{random.choice(answer_options)}'
                    }
                })
                fsm.set_state(user_id, MainGroup.Water.state_1)

            elif 'сон' in command or 'сна' in command or 'фаз' in command:
                res.update({
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
                    'Классно, что Вы решили набрать мышечную массу 🤗. Поздравляю🥳, потому что в скором времени у Вас обязательно будет прекрасное и крепкое тело.'
                    'Хотите выполнить разминку перед тренировкой?',

                    'Мышечная масса способствует развитию силы💪🔥.  Не хотели бы Вы размяться перед основной тренировкой для большего эффекта?']
                res.update({
                    'response': {
                        'text': f'{random.choice(answer_options)}'
                    }
                })
                fsm.set_state(user_id, MainGroup.Sport.Power.state_1)

            elif 'кард' in command:
                answer_options = [
                    'Замечательно! Кардиотренировки несут огромную пользу, а также поднимают настроение. Выберите тип кардио:  классическая или со скакалкой.',

                    'Прекрасный выбор😍! Нагружая сердечно-сосудистую систему, мы укрепляем здоровье. Выберите тип кардио: классическая или со скакалкой.']
                res.update({
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
                res.update({
                    'response': {
                        'text': 'Давайте приступим к кардиотренировке. Для нее вам не понадобится дополнительный инвентарь,'
                                ' не забудьте взять только хорошее настроение и правильный настрой. На каждое упражнение у вас уйдёт по 40 секунд. '
                                'Во время тренировки вы можете изучить упражнение подробнее, выполнить его, или пропустить выполнение и перейти к следующему. '
                                'Вы готовы начать, или рассмотрим другую тренировку?',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': 'Выберите тип кардио'
                            },
                            'items': [
                                {"title": '5-минутная', "button": {"text": '5-минутная'},
                                 "image_id": '1533899/13a130643a2fcdac537a'},
                                {"title": '10-минутная', "button": {"text": '10-минутная'},
                                 "image_id": '1540737/fa873a0d82d3696c73ff'}

                            ]
                        },

                    }
                })
                fsm.set_state(user_id, MainGroup.Sport.Zaradka.state_1)

            else:
                res.update({
                    'response': {
                        'text': 'Извините, не поняла вас😣\nДавайте попробуем заново выбрать занятие!\n'
                                '"Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", или "Фазы сна".',
                        'card': {
                            'type': 'ItemsList',
                            'header': {
                                'text': 'Давайте попробуем заново выбрать занятие!'
                            },
                            'items': [
                                {"title": 'кардиотреннировка', 'button': {"text": 'кардиотреннировка'},
                                 "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                {"title": 'силовая треннировка', "button": {"text": 'силовая треннировка'},
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
        elif fsm.get_state(user_id) in MainGroup.Dream:
            if fsm.get_state(user_id) == MainGroup.Dream.state_1:
                time = parse_time(command)
                go_sleep_times = list(iter_go_sleep_time(time))
                print(time)
                print(go_sleep_times)
                answer_options = [
                    f'Чтобы после сна чувствовать себя полным энергией, Вам следует лечь спать в {go_sleep_times[0].strftime("%H:%M")} '
                    f'или в {go_sleep_times[1].strftime("%H:%M")}😴. Не забудьте завести будильник!',

                    f'Ложитесь спать в {go_sleep_times[0].strftime("%H:%M")} или в {go_sleep_times[1].strftime("%H:%M")}, '
                    f'чтобы утром чувствовать себя полным сил. Не забудьте завести будильник!']
                res.update({
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
        elif fsm.get_state(user_id) in MainGroup.Water:
            if fsm.get_state(user_id) == MainGroup.Water.state_1:
                st = command.replace(',', '.')
                li = st.split(' ')
                for el in li:
                    el = el.replace(',', '.')
                    if el.replace('.', '').isdecimal() and el.count('.') <= 1:
                        answer_options = [
                            f'Ваше минимальное потребление воды {float(el) * 30} миллилитров в день 💦',

                            f'Вам необходимо {float(el) * 30} миллилитров воды 🌊 в день, для хорошего метаболизма. ']
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'Не совсем поняла вас, повторите снова'
                            }
                        })
            elif fsm.get_state(user_id) == MainGroup.Water.end and \
                    ('ещё' in command or 'счит' in command):
                res.update({
                    'response': {
                        'text': 'Скажите свой вес в килограммах'
                    }
                })
                fsm.set_state(user_id, MainGroup.Water.state_1)

        elif fsm.get_state(user_id) in MainGroup.Sport.Cardio:
            if fsm.get_state(user_id) == MainGroup.Sport.Cardio.state_1:
                if 'клас' in command or 'станд' in command or 'перв' in command or 'обычн' in command or 'без' in command:
                    res.update({
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
                    fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.state_1)
                elif 'скак' in command or 'со' in command or 'втор' in command:
                    res.update({
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
                    fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.state_1)
            elif fsm.get_state(user_id) in MainGroup.Sport.Cardio.Solo:
                if fsm.get_state(user_id) == MainGroup.Sport.Cardio.Solo.state_1:
                    if 'нет' in command or 'не ' in command:
                        res.update({
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
                    elif 'да' in command or 'конечн' in command:
                        pass  # TODO: Прописать ветку разминки
                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.start, MainGroup.Sport.Cardio.Solo.final):
                    if 'друг' in command or 'не' in command:
                        res.update({
                            'response': {
                                'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", или "Фазы сна".',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Чем займёмся на этот раз?'
                                    },
                                    'items': [
                                        {"title": 'кардиотреннировка', 'button': {"text": 'кардиотреннировка'},
                                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                        {"title": 'силовая треннировка', "button": {"text": 'силовая треннировка'},
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
                    elif 'да' in command or 'готов' in command or 'повтор' in command:
                        res.update({
                            'response': {
                                'text': 'Начинаем первое упражнение!'
                                        'Поочерёдное сгибание ног с последующим подниманием коленей к груди',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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
                elif fsm.get_state(user_id) in (
                        MainGroup.Sport.Cardio.Solo.task1, MainGroup.Sport.Cardio.Solo.task1_help,
                        MainGroup.Sport.Cardio.Solo.task1_do) or (
                        fsm.get_state(user_id) == MainGroup.Sport.Cardio.Solo.final and 'повтор' in command):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task1_do)
                    elif fsm.get_state(user_id) in (
                            MainGroup.Sport.Cardio.Solo.task1_do, MainGroup.Sport.Cardio.Solo.task1_help,
                            MainGroup.Sport.Cardio.Solo.task1) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Увеличиваем интенсивность тренировки. Выполняем энергичные прыжки с поднятием рук.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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

                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.task2, MainGroup.Sport.Cardio.Solo.task2_help, MainGroup.Sport.Cardio.Solo.task2_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task2_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.task2_do, MainGroup.Sport.Cardio.Solo.task2_help, MainGroup.Sport.Cardio.Solo.task2) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'У вас хорошо получается! Следующее упражнения - бег в планке',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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

                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.task3, MainGroup.Sport.Cardio.Solo.task3_help, MainGroup.Sport.Cardio.Solo.task3_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task3_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.task3_do, MainGroup.Sport.Cardio.Solo.task3_help, MainGroup.Sport.Cardio.Solo.task3) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Приступаем к прыжкам в планке',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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

                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.task4, MainGroup.Sport.Cardio.Solo.task4_help, MainGroup.Sport.Cardio.Solo.task4_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task4_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.task4_do, MainGroup.Sport.Cardio.Solo.task4_help, MainGroup.Sport.Cardio.Solo.task4) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Вы хорошо справляетесь! Далее прыжки из приседа. ',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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

                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.task5, MainGroup.Sport.Cardio.Solo.task5_help, MainGroup.Sport.Cardio.Solo.task5_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task5_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Solo.task5_do, MainGroup.Sport.Cardio.Solo.task5_help, MainGroup.Sport.Cardio.Solo.task5) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Не сбавляем темп тренировки 💪 Далее на очереди упражнение бёрпи. ',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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

                elif fsm.get_state(user_id) in (
                MainGroup.Sport.Cardio.Solo.task6, MainGroup.Sport.Cardio.Solo.task6_help,
                MainGroup.Sport.Cardio.Solo.task6_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task6_do)
                    elif fsm.get_state(user_id) in (
                    MainGroup.Sport.Cardio.Solo.task6_do, MainGroup.Sport.Cardio.Solo.task6_help,
                    MainGroup.Sport.Cardio.Solo.task6) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Переведите дух и выполняйте прыжки с выпадами.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
                                    "title": 'Упражнение 7',
                                    "description": 'Прыжки с выпадами'
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

                elif fsm.get_state(user_id) in (
                        MainGroup.Sport.Cardio.Solo.task7, MainGroup.Sport.Cardio.Solo.task7_help,
                        MainGroup.Sport.Cardio.Solo.task7_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
                            'response': {
                                'text': 'Встаньте в исходное положение, одна нога впереди, другая назад. Держите руки в готовом положении,'
                                        ' согнув локти под углом 90 градусов, одну руку перед собой, а другую назад, чередуя руки и ноги. Например,'
                                        ' если ваша левая нога ведущая, поставьте правую впереди.',
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task7_do)
                    elif fsm.get_state(user_id) in (
                            MainGroup.Sport.Cardio.Solo.task7_do, MainGroup.Sport.Cardio.Solo.task7_help,
                            MainGroup.Sport.Cardio.Solo.task7) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'А сейчас выполняем плиометрический боковой выпад.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
                                    "title": 'Упражнение 8',
                                    "description": 'Плиометрический боковой выпад.'
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

                elif fsm.get_state(user_id) in (
                        MainGroup.Sport.Cardio.Solo.task8, MainGroup.Sport.Cardio.Solo.task8_help,
                        MainGroup.Sport.Cardio.Solo.task8_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
                            'response': {
                                'text': 'Примите классическую стойку. Сделайте широкий шаг правой ногой в сторону, перенесите на нее вес тела, опустите таз до параллели пола. Оттолкнитесь обратно, '
                                        'перенесите вес тела обратно на левую ногу и подпрыгните вверх. Правую ногу не опускайте до конца, а притяните к груди, согнув в колене.',
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task8_do)
                    elif fsm.get_state(user_id) in (
                            MainGroup.Sport.Cardio.Solo.task8_do, MainGroup.Sport.Cardio.Solo.task8_help,
                            MainGroup.Sport.Cardio.Solo.task8) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'И завершающее упражнение! Сделаем выпрыгивания из полувыпада.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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

                elif fsm.get_state(user_id) in (
                        MainGroup.Sport.Cardio.Solo.task9, MainGroup.Sport.Cardio.Solo.task9_help,
                        MainGroup.Sport.Cardio.Solo.task9_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.task9_do)
                    elif fsm.get_state(user_id) in (
                            MainGroup.Sport.Cardio.Solo.task9_do, MainGroup.Sport.Cardio.Solo.task9_help,
                            MainGroup.Sport.Cardio.Solo.task9) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        answer_options = ['Заминка нужна, чтобы снизить до нормального уровня частоту сердечных сокращений. Хотите её выпонить?',
                                          'Будет здорово выполнить заминку! Заминка снижает склонность к закрепощению мышц после нагрузки.  Хотели бы Вы приступить к её выполнению?']
                        res.update({
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

                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.end)

                elif fsm.get_state(user_id) == MainGroup.Sport.Cardio.Solo.end:
                        if 'нет' in command or 'не ' in command:
                            res.update({
                                'response': {
                                    'text': 'Вы хорошо потрудились, горжусь Вами. Повторим тренировку или вернёмся в меню? Выбор за Вами.',
                                    'card': {
                                        'type': 'ItemsList',
                                        'header': {
                                            'text': 'Повторим тренировку или вернёмся в меню?'
                                        },
                                        'items': [
                                            {"title": 'Повторить треннировку', "button": {"text": 'Повторить треннировку'},
                                             "image_id": '997614/15f977696a281092bcc0'},
                                            {"title": 'Вернуться в меню',
                                             "button": {"text": 'Вернуться в меню'},
                                             "image_id": '1030494/cc3631c8499cdc8daf8b'}

                                        ]
                                    }

                                }
                            })
                            fsm.set_state(user_id, MainGroup.Sport.Cardio.Solo.final)
                        elif 'да' in command or 'конечн' in command:
                            pass  # TODO: Прописать ветку зазминки

            elif fsm.get_state(user_id) in MainGroup.Sport.Cardio.Rope:
                if fsm.get_state(user_id) == MainGroup.Sport.Cardio.Rope.state_1:
                    if 'нет' in command or 'не ' in command:
                        res.update({
                            'response': {
                                'text': 'Давайте приступим к кардиотренировке. Для нее Вам понадобится только скакалка и хорошее настроение.'
                                        ' Одно упражнение занимает 40 секунд. Перед тем, как его проделать, Вы можете изучить технику подробнее,'
                                        ' начать выполнение или пропустить его и перейти к следующему.Вы готовы к кардио или подберём другую тренировку?',
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
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.start)
                    elif 'да' in command or 'конечн' in command:
                        pass  # TODO: Прописать ветку разминки
                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.start, MainGroup.Sport.Cardio.Rope.final):
                    if 'друг' in command or 'не' in command:
                        res.update({
                            'response': {
                                'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", или "Фазы сна".',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Чем займёмся на этот раз?'
                                    },
                                    'items': [
                                        {"title": 'кардиотреннировка', 'button': {"text": 'кардиотреннировка'},
                                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                        {"title": 'силовая треннировка', "button": {"text": 'силовая треннировка'},
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
                    elif 'да' in command or 'готов' in command or 'повтор' in command:
                        res.update({
                            'response': {
                                'text': 'Начинаем нашу энергичную тренировку с прыжков на скакалке.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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
                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task1, MainGroup.Sport.Cardio.Rope.task1_help, MainGroup.Sport.Cardio.Rope.task1_do) or (fsm.get_state(user_id) == MainGroup.Sport.Cardio.Rope.final and 'повтор' in command):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task1_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task1_do, MainGroup.Sport.Cardio.Rope.task1_help, MainGroup.Sport.Cardio.Rope.task1) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Продолжаем тренировку! Начинаем отжимания.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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
                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task2, MainGroup.Sport.Cardio.Rope.task2_help, MainGroup.Sport.Cardio.Rope.task2_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task2_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task2_do, MainGroup.Sport.Cardio.Rope.task2_help,MainGroup.Sport.Cardio.Rope.task2) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'У Вас прекрасно получается! Продолжаем укреплять своё тело: делаем приседания с выпрыгиванием.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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
                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task3, MainGroup.Sport.Cardio.Rope.task3_help, MainGroup.Sport.Cardio.Rope.task3_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task3_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task3_do, MainGroup.Sport.Cardio.Rope.task3_help,MainGroup.Sport.Cardio.Rope.task3) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Это было круто! А теперь знакомые прыжки на скакалке.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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
                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task4, MainGroup.Sport.Cardio.Rope.task4_help, MainGroup.Sport.Cardio.Rope.task4_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task4_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task4_do, MainGroup.Sport.Cardio.Rope.task4_help,MainGroup.Sport.Cardio.Rope.task4) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Ура, завершающее упражнение! Последний рывок - поднятие коленей к груди в прыжке с полувыпадами.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
                                    "title": 'Упражнение 4',
                                    "description": 'Поднятие коленей к груди в прыжке с полувыпадами'
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
                elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task5, MainGroup.Sport.Cardio.Rope.task5_help, MainGroup.Sport.Cardio.Rope.task5_do):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
                            'response': {
                                'text': 'Сделав небольшой шаг назад, опуститесь в полувыпад. Затем оттолкнитесь и в прыжке поднимите колено отведенной ноги до уровня груди. Руки двигаются вдоль тела, как во время бега.',
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
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.task5_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Cardio.Rope.task5_do, MainGroup.Sport.Cardio.Rope.task5_help,MainGroup.Sport.Cardio.Rope.task5) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        answer_options = [
                            'Заминка нужна, чтобы снизить до нормального уровня частоту сердечных сокращений. Хотите её выпонить?',
                            'Будет здорово выполнить заминку! Заминка снижает склонность к закрепощению мышц после нагрузки.  Хотели бы Вы приступить к её выполнению?']
                        res.update({
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

                        fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.end)
                elif fsm.get_state(user_id) == MainGroup.Sport.Cardio.Rope.end:
                        if 'нет' in command or 'не ' in command:
                            res.update({
                                'response': {
                                    'text': 'Вы хорошо потрудились, горжусь Вами. Повторим тренировку или вернёмся в меню? Выбор за Вами.',
                                    'card': {
                                        'type': 'ItemsList',
                                        'header': {
                                            'text': 'Повторим тренировку или вернёмся в меню?'
                                        },
                                        'items': [
                                            {"title": 'Повторить треннировку', "button": {"text": 'Повторить треннировку'},
                                             "image_id": '997614/15f977696a281092bcc0'},
                                            {"title": 'Вернуться в меню',
                                             "button": {"text": 'Вернуться в меню'},
                                             "image_id": '1030494/cc3631c8499cdc8daf8b'}

                                        ]
                                    }

                                }
                            })
                            fsm.set_state(user_id, MainGroup.Sport.Cardio.Rope.final)
                        elif 'да' in command or 'конечн' in command:
                            pass  # TODO: Прописать ветку зазминки

        elif fsm.get_state(user_id) in MainGroup.Sport.Zaradka:
            if fsm.get_state(user_id) == MainGroup.Sport.Zaradka.state_1:
                if 'пят' in command or '5' in command:
                    res.update({
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
                    res.update({
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
            elif fsm.get_state(user_id) in MainGroup.Sport.Zaradka.Five:
                if fsm.get_state(user_id) in (MainGroup.Sport.Zaradka.Five.start, MainGroup.Sport.Zaradka.Five.final):
                    if 'друг' in command or 'не' in command:
                        res.update({
                            'response': {
                                'text': 'Чем займёмся на этот раз? Выбирайте: "Кардиотренировка", "Силовая тренировка", "Утренняя зарядка", "Водный баланс", или "Фазы сна".',
                                'card': {
                                    'type': 'ItemsList',
                                    'header': {
                                        'text': 'Чем займёмся на этот раз?'
                                    },
                                    'items': [
                                        {"title": 'кардиотреннировка', 'button': {"text": 'кардиотреннировка'},
                                         "description": 'описание...', "image_id": '1533899/13a130643a2fcdac537a'},
                                        {"title": 'силовая треннировка', "button": {"text": 'силовая треннировка'},
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
                    elif 'да' in command or 'готов' in command or 'повтор' in command:
                        res.update({
                            'response': {
                                'text': 'Приступаем  к растиранию шеи!',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task1)
                elif fsm.get_state(user_id) in (MainGroup.Sport.Zaradka.Five.task1, MainGroup.Sport.Zaradka.Five.task1_help, MainGroup.Sport.Zaradka.Five.task1_do) or (fsm.get_state(user_id) == MainGroup.Sport.Zaradka.Five.final and 'повтор' in command):
                    if 'подробн' in command or 'объяс' in command:
                        res.update({
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
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task1_help)
                    elif 'выполн' in command or 'дел' in command:
                        res.update({
                            'response': {
                                'text': f'{random.choice(motivation)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task1_do)
                    elif fsm.get_state(user_id) in (MainGroup.Sport.Zaradka.Five.task1_do, MainGroup.Sport.Zaradka.Five.task1_help, MainGroup.Sport.Zaradka.Five.task1) and ('проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        res.update({
                            'response': {
                                'text': 'Это было легко. Постепенно усложняемся и переходим к наклонам головы.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/75d7fd59f370ba0f15f3',
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
                        fsm.set_state(user_id, MainGroup.Sport.Zaradka.Five.task2)


    else:
        res.update({
            'response': {
                'text': f'Произошла ошибка. Скажите "поехали" чтобы вернуться в главное меню.'
            }
        })
        fsm.set_state(user_id, MainGroup.state_1)

    return dict_to_json(res, ensure_ascii=False, indent=2)


app.run('localhost', port=5050, debug=True)
