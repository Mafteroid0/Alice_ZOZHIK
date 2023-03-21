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
                    'text': f'{answer_options[rn.randint(0, 1)]} \nДля продолжения скажите "поехали!"',
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

        if fsm.get_state(user_id) == MainGroup.state_1 and req['request'][
            'command'] == 'поехали':  # TODO: Добавить в условия номера стейтов, из которых можно сюда попасть (см. диаграмму)
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
            print('HELLO', fsm.get_state(user_id))


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
            fsm.set_state(user_id, MainGroup.state_1)
        return json.dumps(res, ensure_ascii=False, indent=2)


app.run('localhost', port=5050, debug=True)
