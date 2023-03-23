import json
import random as rn

import typing
from flask import Flask, request

from typing_ import FriendlyDict, AliceUserRequest
from fsm import StatesGroup, State, FSM

app = Flask(__name__)

fsm = FSM()


def dict_to_json(dict_: dict, *args, **kwargs):
    for key, value in dict_.items():
        if isinstance(value, FriendlyDict):
            dict_[key] = value.to_dict()
    return json.dumps(dict_, *args, **kwargs)


class MainGroup(StatesGroup):  # Состояние по умолчанию это None, его не нужно явно определять
    _fsm = fsm
    state_1 = State()

    class SportBranch(StatesGroup):
        state_home = State()

        class Water(StatesGroup):
            state_1 = State()
            end = State()

        class Dream(StatesGroup):
            state_1 = State()

        class Power(StatesGroup):
            state_1 = State()

        class Cardio(StatesGroup):
            state_1 = State()

        class Zaradka(StatesGroup):
            state_1 = State()


# Шаблон для условий:  if fsm.get_state(user_id) == MyStates.state_1
# Диаграмма: https://miro.com/app/board/uXjVMdrXZW0=/

@app.route('/alice', methods=['POST'])
def main():
    end = False
    req = AliceUserRequest(request.data.decode())
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
                'text': f'{answer_options[rn.randint(0, 1)]}',
                'buttons': [
                    {
                        'title': 'Что ты умеешь?',
                        'hide': True
                    },
                    {
                        "title": "Поехали",
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
                'text': f'{answer_options[rn.randint(0, 1)]} \n',
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

    elif (fsm.get_state(user_id) == MainGroup.state_1 or fsm.get_state(
            user_id) is None) and command == 'поехали':  # TODO: Добавить в условия номера стейтов, из которых можно сюда попасть (см. диаграмму)
        answer_options = ['Вау, Вы уже в нескольких шагах от здоровый образа жизни очень рада за Вас  😍. '
                          'Для начала выберите, чем хотите заняться или что Вам нужно узнать:'
                          ' "Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".',

                          'Вы уже совсем-совсем близко к здоровой жизни 😍, горжусь Вами. '
                          'Время выбирать, чем хотите заняться или что Вам нужно узнать:\n'
                          '"Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".']
        res.update({
            'response': {
                'text': f'{answer_options[rn.randint(0, 1)]}',
                'buttons': [
                    {
                        'title': 'Зарядка',
                        'hide': True
                    },
                    {
                        "title": "Кардиотренировка",
                        "hide": True
                    },
                    {
                        "title": "Силовая фуллбади тренировка",
                        "hide": True
                    },
                    {
                        'title': 'Фазы сна',
                        'hide': True
                    },
                    {
                        'title': 'Водный баланс',
                        'hide': True
                    }
                ]
            }
        })
        fsm.set_state(user_id, MainGroup.SportBranch.state_home)

    elif fsm.get_state(user_id) in MainGroup.SportBranch:
        if fsm.get_state(user_id) == MainGroup.SportBranch.state_home:
            if 'вод' in command or 'баланс' in command:
                answer_options = [
                    'Вода жизненно необходима каждому человеку, а употребление её дневной нормы улучшает метаболизм.'
                    ' Я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. '
                    'Для того, чтобы точно рассчитать минимальное объём воды, мне необходимо знать вес человека. '
                    'Подскажите, пожалуйста, вес Вашего тела в килограммах.',

                    'Так как мы состоим из воды примерно на 70% 🐳, то употреблять её в достаточном количестве очень важно. '
                    'Не переживайте 😉 , я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. '
                    'Для того, чтобы точно рассчитать минимальное объём воды, мне нужен вес человека. Подскажите, пожалуйста, вес Вашего тела в килограммах.']

                res.update({
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                })
                fsm.set_state(user_id, MainGroup.SportBranch.Water.state_1)

            elif 'сон' in command or 'сна' in command or 'фаз' in command:
                res.update({
                    'response': {
                        'text': 'Здорово🥰 , что Вы решили следить за своим сном, так как он играет важную роль в нашей жизни 🛌.'
                                'Напишите, во сколько вы хотите проснуться (формат времени от 0:00 до 23:59),'
                                ' а я Вам подскажу идеальное время, когда необходимо будет лечь спать, чтобы проснуться бодрым.'
                    }
                })
                fsm.set_state(user_id, MainGroup.SportBranch.Dream.state_1)
                print('SON?')

            elif 'сил' in command:
                answer_options = [
                    'Классно, что Вы решили набрать мышечную массу 🤗. Поздравляю🥳, потому что в скором времени у Вас обязательно будет прекрасное и крепкое тело.'
                    'Хотите выполнить разминку перед тренировкой?',

                    'Мышечная масса способствует развитию силы💪🔥.  Не хотели бы Вы размяться перед основной тренировкой для большего эффекта?']
                res.update({
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                })
                fsm.set_state(user_id, MainGroup.SportBranch.Power.state_1)

            elif 'кард' in command:
                answer_options = [
                    'Замечательно! Кардиотренировки несут огромную пользу, а также поднимают настроение🥳. Выберите тип кардио:  классическая или со скакалкой.',

                    'Прекрасный выбор😍! Нагружая сердечно-сосудистую систему, мы укрепляем здоровье. Выберите тип кардио: классическая или со скакалкой.']
                res.update({
                    'version': req['version'],
                    'session': req['session'],
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                })
                fsm.set_state(user_id, MainGroup.SportBranch.Cardio.state_1)

            elif 'заряд' in command:
                answer_options = [
                    'Зарядка оказывает комплексное воздействие на организм. Она активизирует кровообращение,'
                    ' ускоряет обмен веществ. Давайте вместе привидём ваше тело в тонус💪. Выберите тип зарядки:  5-минутная или 10-минутная.',

                    'Отличный выбор 🤩. Зарядка нужна всем, но немногие это понимают, к счастью к Вам это не относится. Выберите тип зарядки: 5-минутная или 10-минутная.',

                    'Прекрасно🔥! Держать тело в форме необходимо всем, очень приятно, что Вы это понимаете😊. Однако зарядки тоже бывают разными. Какую тип зарядки хотите: 5-минутная или 10-минутная.']
                res.update({
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                })
                fsm.set_state(user_id, MainGroup.SportBranch.Zaradka.state_1)

            else:
                res.update({
                    'response': {
                        'text': f'Извините, не поняла вас😣\nДавайте попробуем заново выбрать занятие!\n'
                                f'"Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс" ',
                        'buttons': [
                            {
                                'title': 'Зарядка',
                                'hide': True
                            },
                            {
                                "title": "Кардиотренировка",
                                "hide": True
                            },
                            {
                                "title": "Силовая фуллбади тренировка",
                                "hide": True
                            },
                            {
                                'title': 'Фазы сна',
                                'hide': True
                            },
                            {
                                'title': 'Водный баланс',
                                'hide': True
                            }
                        ]
                    }
                })
                fsm.set_state(user_id, MainGroup.SportBranch.state_home)
        elif fsm.get_state(user_id) in MainGroup.SportBranch.Dream:
            print('SON')
            if fsm.get_state(user_id) == MainGroup.SportBranch.Dream.state_1:
                def timeplus(hhmm: str):
                    _time = list(map(int, hhmm.split(':')))
                    _time1 = _time.copy()

                    _time[1] -= 45
                    if _time[1] < 0:
                        _time[0] -= 1
                        _time[1] += 60
                    _time[0] -= 7
                    if _time[0] < 0:
                        _time[0] += 24
                    _time = list(map(str, _time))
                    if len(_time[1]) == 1:
                        _time[1] = f'0{_time[1]}'

                    _time1[1] -= 15
                    if _time1[1] < 0:
                        _time1[0] -= 1
                        _time1[1] += 60
                    _time1[0] -= 9
                    if _time1[0] < 0:
                        _time1[0] += 24
                    _time1 = list(map(str, _time1))
                    if len(_time1[1]) == 1:
                        _time1[1] = f'0{_time1[1]}'
                    return [f'{_time[0]}:{_time[1]}', f'{_time1[0]}:{_time1[1]}']
                print(command)
                print(timeplus(command))
                answer_options = [
                    f'Чтобы после сна чувствовать себя полным энергией, Вам следует лечь спать в {timeplus(command)[0]} или в {timeplus(command)[1]}😴',

                    f'Ложитесь спать в {timeplus(command)[0]} или в {timeplus(command)[1]}, чтобы утром чувствовать себя полным сил.']
                res.update({
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                })
        elif fsm.get_state(user_id) in MainGroup.SportBranch.Water:
            if fsm.get_state(user_id) == MainGroup.SportBranch.Water.state_1:
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
                                'text': f'{answer_options[rn.randint(0, 1)]}',
                                'buttons': [
                                    {
                                        'title': 'Рассчитать ещё раз',
                                        'hide': True
                                    },
                                    {
                                        "title": "Вернуться к основному списку",
                                        "hide": True
                                    }
                                ]
                            }
                        })
                        fsm.set_state(user_id, MainGroup.SportBranch.Water.end)
                        break
                    else:
                        res.update({
                            'response': {
                                'text': f'Не совсем поняла вас, повторите снова'
                            }
                        })
            elif fsm.get_state(user_id) == MainGroup.SportBranch.Water.end:
                if 'вернуться' in command or 'назад' in command or 'основ' in command:
                    res.update({
                        'response': {
                            'text': 'Чем займёмся на этот раз? Выбирайте: "Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".',
                            'buttons': [
                                {
                                    'title': 'Зарядка',
                                    'hide': True
                                },
                                {
                                    "title": "Кардиотренировка",
                                    "hide": True
                                },
                                {
                                    "title": "Силовая фуллбади тренировка",
                                    "hide": True
                                },
                                {
                                    'title': 'Фазы сна',
                                    'hide': True
                                },
                                {
                                    'title': 'Водный баланс',
                                    'hide': True
                                }
                            ]
                        }
                    })
                    fsm.set_state(user_id, MainGroup.SportBranch.state_home)

                elif (fsm.get_state(user_id) == MainGroup.SportBranch.Water.end and (
                        'ещё' in command or 'счит' in command)):
                    res.update({
                        'response': {
                            'text': 'Скажите свой вес в килограммах'
                        }
                    })
                    fsm.set_state(user_id, MainGroup.SportBranch.Water.state_1)


    else:
        res.update({
            'response': {
                'text': f'Произошла ошибка. Скажите "поехали" чтобы вернуться в главное меню.'
            }
        })
        fsm.set_state(user_id, MainGroup.state_1)

    return dict_to_json(res, ensure_ascii=False, indent=2)


app.run('localhost', port=5050, debug=True)
