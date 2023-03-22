import json
import random as rn

from flask import Flask, request

from fsm import StatesGroup, State, FSM

app = Flask(__name__)

fsm = FSM()


class MainGroup(StatesGroup):  # Состояние по умолчанию это None, его не нужно явно определять
    _fsm = fsm
    state_1 = State()

    class SportBranch(StatesGroup):
        state_home = State()

        class Water(StatesGroup):
            state_1 = State()

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

    req = json.loads(request.data)
    user_id = req['session']['user']['user_id']  # TODO: тут впиши путь до айди юзера
    print(fsm.get_state(user_id))
    if req['session']['new']:
        # Действия при новой сессии
        res = {
            'version': req['version'],
            'session': req['session'],
            'response': {
                'text': 'Привет🖐!  Всегда хотели окунуться в мир здорового образа жизни? '
                        'Поздравляю, Вы сделали правильный выбор.'
                        'Я навык ... помогу освоить основы ЗОЖ на практике с лёгкостью и удовольствием.'
                        'Если хотите ознакомиться с моим функционалом, то скажите "Что ты умеешь?". Если же готовы приступить, то скажите "Поехали".',
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
        }
        fsm.reset_state(user_id)
        return json.dumps(res, ensure_ascii=False, indent=2)
    else:
        res = []  # TODO: Потом заменим на сообщение об ошибке
        if fsm.get_state(user_id) == None and (req['request']['command'] == 'что ты умеешь'):
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

            res = {
                'version': req['version'],
                'session': req['session'],
                'response': {
                    'text': f'{answer_options[rn.randint(0, 1)]} \n',
                    'buttons': [
                        {
                            'title': 'Поехали!',
                            'hide': True
                        }
                    ]

                }
            }
            fsm.set_state(user_id, MainGroup.state_1)
            return json.dumps(res, ensure_ascii=False, indent=2)

        if (fsm.get_state(user_id) == MainGroup.state_1  or fsm.get_state(user_id) == None) and req['request']['command'] == 'поехали':  # TODO: Добавить в условия номера стейтов, из которых можно сюда попасть (см. диаграмму)
            answer_options = ['Вау, Вы уже в нескольких шагах от ЗОЖа 😍, '
                              'очень рада за Вас. Для начала выберите, чем хотите заняться'
                              ' или что Вам нужно узнать:\n'
                              '"Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".',

                              'Вы уже совсем-совсем близко к здоровой жизни 😍, горжусь Вами. '
                              'Время выбирать, чем хотите заняться или что Вам нужно узнать:\n'
                              '"Зарядка", "Кардио", "Силовая", "Фазы сна" или "Водный баланс".']
            res = {
                'version': req['version'],
                'session': req['session'],
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
            }
            fsm.set_state(user_id, MainGroup.SportBranch.state_home)
            print(fsm.get_state(user_id))

        if fsm.get_state(user_id) in MainGroup.SportBranch:
            if fsm.get_state(user_id) == MainGroup.SportBranch.state_home and ('вод' in req['request']['command'] or 'баланс' in req['request']['command']):
                answer_options = ['Вода жизненно необходима каждому человеку, а употребление её дневной нормы улучшает метаболизм.'
                                  ' Я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. '
                                  'Для того, чтобы точно рассчитать минимальное объём воды, мне необходимо знать вес человека. '
                                  'Подскажите, пожалуйста, вес Вашего тела.',

                                  'Так как мы состоим из воды примерно на 70% 🐳, то употреблять её в достаточном количестве очень важно. '
                                  'Не переживайте 😉 , я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. '
                                  'Для того, чтобы точно рассчитать минимальное объём воды, мне нужен вес человека. Подскажите, пожалуйста, вес Вашего тела.']
                res = {
                    'version': req['version'],
                    'session': req['session'],
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                }
                fsm.set_state(user_id, MainGroup.SportBranch.Water.state_1)

            elif fsm.get_state(user_id) == MainGroup.SportBranch.state_home and ('сон' in req['request']['command'] or 'сна' in req['request']['command'] or 'фаз' in req['request']['command']):
                res = {
                    'version': req['version'],
                    'session': req['session'],
                    'response': {
                        'text': 'Здорово🥰 , что Вы решили следить за своим сном, так как он играет важную роль в нашей жизни 🛌.'
                                'Напишите, во сколько вы хотите проснуться (формат времени от 0:00 до 23:59),'
                                ' а я Вам подскажу идеальное время, когда необходимо будет лечь спать, чтобы проснуться бодрым.'
                    }
                }
                fsm.set_state(user_id, MainGroup.SportBranch.Dream.state_1)

            elif fsm.get_state(user_id) == MainGroup.SportBranch.state_home and ('сил' in req['request']['command']):
                answer_options = [
                    'Классно, что Вы решили набрать мышечную массу 🤗. Поздравляю🥳, потому что в скором времени у Вас обязательно будет прекрасное и крепкое тело.'
                    'Хотите выполнить разминку перед тренировкой?',

                    'Мышечная масса способствует развитию силы💪🔥.  Не хотели бы Вы размяться перед основной тренировкой для большего эффекта?']
                res = {
                    'version': req['version'],
                    'session': req['session'],
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                }
                fsm.set_state(user_id, MainGroup.SportBranch.Power.state_1)

            elif fsm.get_state(user_id) == MainGroup.SportBranch.state_home and ('кард' in req['request']['command']):
                answer_options = [
                    'Замечательно! Кардиотренировки несут огромную пользу, а также поднимают настроение🥳. Выберите тип кардио:  классическая или со скакалкой.',

                    'Прекрасный выбор😍! Нагружая сердечно-сосудистую систему, мы укрепляем здоровье. Выберите тип кардио: классическая или со скакалкой.']
                res = {
                    'version': req['version'],
                    'session': req['session'],
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                }
                fsm.set_state(user_id, MainGroup.SportBranch.Cardio.state_1)

            elif fsm.get_state(user_id) == MainGroup.SportBranch.state_home and ('заряд' in req['request']['command']):
                answer_options = [
                    'Зарядка оказывает комплексное воздействие на организм. Она активизирует кровообращение,'
                    ' ускоряет обмен веществ. Давайте вместе привидём ваше тело в тонус💪. Выберите тип зарядки:  5-минутная или 10-минутная.',

                    'Отличный выбор 🤩. Зарядка нужна всем, но немногие это понимают, к счастью к Вам это не относится. Выберите тип зарядки: 5-минутная или 10-минутная.',

                    'Прекрасно🔥! Держать тело в форме необходимо всем, очень приятно, что Вы это понимаете😊. Однако зарядки тоже бывают разными. Какую тип зарядки хотите: 5-минутная или 10-минутная.']
                res = {
                    'version': req['version'],
                    'session': req['session'],
                    'response': {
                        'text': f'{answer_options[rn.randint(0, 1)]}'
                    }
                }
                fsm.set_state(user_id, MainGroup.SportBranch.Zaradka.state_1)

        else:
            res = {
                'version': req['version'],
                'session': req['session'],
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
            }
            fsm.set_state(user_id, MainGroup.SportBranch.state_home)
        return json.dumps(res, ensure_ascii=False, indent=2)


app.run('localhost', port=5050, debug=True)
