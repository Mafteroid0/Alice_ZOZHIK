import random

from handlers.main_menu import show_main_menu
from typing_ import Response, AliceUserRequest, ResponseField, Card, CardType, Item, Button
from fsm import FSMContext

from dialogs import MOTIVATIONS, TRACKS_FOURTEEN

from states import MainGroup


def _start_solo_cardio(context: FSMContext, resp: dict | Response) -> dict | Response:
    resp.response = ResponseField(
        text=['Давайте приступим к кардиотренировке. Для нее вам не понадобится дополнительный инвентарь,'
              'не забудьте взять только хорошее настроение и правильный настрой. На каждое упражнение у вас '
              'уйдёт по 40 секунд.'
              'Во время тренировки вы можете изучить упражнение подробнее, выполнить его, или пропустить '
              'выполнение и перейти к следующему.'
              'Вы готовы начать, или рассмотрим другую тренировку?',

              'Начнем нашу кардиотренировку. Она не предполагает использование дополнительного инвентаря. Каждое '
              'упражнение необходимо выполнять 40 секунд. Во время тренировки Вы можете воспользоваться функцией '
              '"подробнее", чтобы ознакомиться с техникой выполнения упражнения, начать выполнять его или пропустить '
              'текущее упражнение и перейти к следующему.'
              'Вы готовы или выберем что-нибудь другое? '],
        card=Card(
            type=CardType.ItemsList, header='Приступаем к выполнению кардиотренировки',
            items=[
                Item(title='Я готов', button='Я готов', image_id='997614/72ab6692a3db3f4e3056'),
                Item(title='Выберем другую тренировку', button='Выберем другую тренировку',
                     image_id='1030494/cc3631c8499cdc8daf8b')
            ]
        )
    )
    context.set_state(MainGroup.Sport.Cardio.Solo.start)
    return resp


def _finish_solo_cardio(context: FSMContext, resp: dict | Response) -> dict | Response:
    resp.response = ResponseField(
        text=['Вы хорошо потрудились, горжусь Вами. Повторим тренировку или вернёмся в меню? Выбор за Вами.',

              'Вы прекрасно потрудились. Что хотите сделать дальше: повторить тренировку или завершить её?'],
        card=Card(
            type=CardType.ItemsList,
            header='Повторим тренировку или вернёмся в меню?',
            items=[
                Item(
                    title='Повторить тренировку',
                    button='Повторить тренировку',
                    image_id='997614/15f977696a281092bcc0'
                ),
                Item(
                    title='Вернуться в меню',
                    button='Вернуться в меню',
                    image_id='1030494/cc3631c8499cdc8daf8b'
                )
            ]
        )
    )
    context.set_state(MainGroup.Sport.Cardio.Solo.final)
    return resp


def _start_rope_cardio(context: FSMContext, resp: dict | Response) -> dict | Response:
    answer_options = ["Давайте приступим к кардиотренировке. Для нее Вам понадобится только скакалка и хорошее настроение. Одно упражнение занимает 40 секунд."
                    " Перед тем, как его проделать, Вы можете изучить технику подробнее, начать выполнение или пропустить его и перейти к следующему.Вы готовы к кардио или подберём другую тренировку?",
                    "Поехали! Для тренировки приготовьте скакалку. Для одного упражнения нужно 40 секунд. Перед тем, как его сделать, "
                    "Вы можете изучить технику подробнее, начать выполнение или пропустить его и перейти к следующему. Вы готовы к кардио или выберите что-то другое?"]
    resp.update({
        'response': {
            'text': f'{random.choice(answer_options)}',
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
    context.set_state(MainGroup.Sport.Cardio.Rope.start)
    return resp


def finish_rope_cardio(context: FSMContext, resp: dict | Response) -> dict | Response:
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
    context.set_state(MainGroup.Sport.Cardio.Rope.final)
    return resp


def cardio_handler(context: FSMContext, req: AliceUserRequest, resp: dict | Response) -> dict | Response:
    state = context.state
    command = req.request.command

    if state == MainGroup.Sport.Cardio.state_1:
        resp.response = ResponseField(
            text=[
                'Хотите выполнить разминку перед тренировкой?',
                'Хотите подготовиться к тяжёлым нагрузкам с помощью разминки?', 'Может подготовим Ваше тело к нагрузкам с помощью несложной разминки?'
            ],
            card=Card(
                type=CardType.ItemsList,
                header='Хотите выполнить разминку?',
                items=[
                    Item(title='Выполнить разминку', button='Да', image_id='213044/9c13b9b997d78cde2579'),
                    Item(title='Продолжить без разминки', button='Нет', image_id='1540737/cc47e154fc7c83b6ba0d')
                ]
            )
        )
        if 'клас' in command or 'станд' in command or 'перв' in command or 'обычн' in command or 'без' in command:
            context.update_data(callback=_start_solo_cardio)
            context.set_state(MainGroup.Sport.Wrap.WarmUp.qw)
        elif 'скак' in command or 'со' in command or 'втор' in command:
            context.update_data(callback=_start_rope_cardio)
            context.set_state(MainGroup.Sport.Wrap.WarmUp.qw)
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
                show_main_menu(context, resp)
            elif 'да' in command or 'готов' in command or 'повтор' in command or 'нач' in command or 'запус' in command:
                resp.response = ResponseField(
                    text=[
                        "Начинаем первое упражнение!"
                        "Поочерёдное сгибание ног с последующим подниманием коленей к груди",

                        'Начать тренировку предлагаю с поочерёдного сгибания ноги с последующим подниманием коленей к '
                        'груди.'
                    ],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='997614/15bfafd8b629b323890b',
                        title='Упражнение 1',
                        description='Поочерёдное сгибание ног с последующим подниманием коленей к груди'
                    ),
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task1)
            else:
                resp.update({
                    'response': {
                        'text': 'Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение тренировки, или возвращаемся в меню?',
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
                context.set_state(MainGroup.Sport.Cardio.Solo.task1_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task1_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task1_do, MainGroup.Sport.Cardio.Solo.task1_help,
                    MainGroup.Sport.Cardio.Solo.task1) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                resp.response = ResponseField(
                    text=[
                        'Увеличиваем интенсивность тренировки. Выполняем энергичные прыжки с поднятием рук.',

                        'Постепенно увеличиваем нагрузку. Делаем прыжки с поднятием рук.'
                    ],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='1540737/6cd05842046b48c768bc',
                        title='Упражнение 2',
                        description='Энергичные прыжки с поднятием рук.'
                    ),
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ])
                context.set_state(MainGroup.Sport.Cardio.Solo.task2)
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
                resp.response = ResponseField(
                    text=['Стопы поставьте плотно вместе, а руки вдоль туловища. Выполните два движения вместе:'
                          'в прыжке расставьте широко ноги и вытяните вверх руки, сводя их вместе над головой. Прыжком '
                          'вернитесь в начальную позу.',

                          'Встаньте прямо, стопы сведены вместе, руки опущены.'
                          'Согните колени и сделайте прыжок. В прыжке одновременно разведите ноги чуть шире плеч и поднимите руки через стороны вверх, можете сделать хлопок на головой.'],
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task2_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task2_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task2_do, MainGroup.Sport.Cardio.Solo.task2_help,
                    MainGroup.Sport.Cardio.Solo.task2) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                resp.response = ResponseField(
                    text=[
                        'У вас хорошо получается!🔥 Следующего упражнения - бег в планке.',

                        'Не сбавляйте темп! Приступаем к бегу в планке.'
                    ],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='1030494/94bcca53f06da5b24f90',
                        title='Упражнение 3',
                        description='Бег в планке'
                    ),
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task3)
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
                resp.response = ResponseField(
                    text=['Для следующего упражнения встаньте в планку на прямых руках. Начните имитировать бег '
                          '– по очереди подтягивайте колени к груди. Ноги ставьте на носки, линию позвоночника '
                          'не меняйте.',

                          'Встаньте в положении планки на руках, ладони точно под плечами. Подтяните правое '
                          'колено к груди, при этом напрягите мышцы пресса еще сильнее (это поможет сохранить '
                          'тело в правильном положении). Легкой подпрыжкой подтяните левое колено к груди, '
                          'имитируя бег в положении планки.'],
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task3_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task3_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task3_do, MainGroup.Sport.Cardio.Solo.task3_help,
                    MainGroup.Sport.Cardio.Solo.task3) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                resp.response = ResponseField(
                    text=['Приступаем к прыжкам в планке',

                          'Не останавливайтесь! Теперь делаем прыжки в планке.'],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='213044/bf1b200f757b3aae40df',
                        title='Упражнение 4',
                        description='Прыжки в планке'
                    ),
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task4)
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
                context.set_state(MainGroup.Sport.Cardio.Solo.task4_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task4_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task4_do, MainGroup.Sport.Cardio.Solo.task4_help,
                    MainGroup.Sport.Cardio.Solo.task4) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                resp.response = ResponseField(
                    text=['Вы хорошо справляетесь! Далее идут прыжки из приседа.',

                          'Здорово! Выполняйте прыжки из приседа.'],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='937455/b69ef8ea88fa63b48c20',
                        title='Упражнение 5',
                        description='прыжки из приседа.'
                    ),
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task5)
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
                resp.response = ResponseField(
                    text=['Начните из положения стоя, ноги на ширине плеч. Выполните приседание и выведите руки '
                          'вперед. Выпрыгивайте, одновременно выпрямляя руки.',

                          'Поставьте ноги на ширину плеч, выпрямите спину.'
                          'Присед делается на вдохе. На выдохе необходимо сделать мощное выпрыгивание вверх, '
                          'оттолкнувшись полными ступнями. После того как ваши стопы полностью коснулись пола, '
                          'снова уйдите в присед.'],
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task5_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task5_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task5_do, MainGroup.Sport.Cardio.Solo.task5_help,
                    MainGroup.Sport.Cardio.Solo.task5) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                resp.response = ResponseField(
                    text=['Не сбавляем темп 💪. Далее на очереди упражнение бёрпи.',

                          'У Вас отлично получается. Начинайте выполнять упражнение бёрпи.'],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='997614/538aaaa7db557abbda82',
                        title='Упражнение 6',
                        description='упражнение бёрпи.'
                    ), buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task6)
            else:
                resp.update({
                    'response': {
                        'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                resp.response = ResponseField(
                    text=['Подпрыгните, отведите ноги назад и опустите таз, чтобы получилась поза планки. Соберитесь '
                          'обратно прыжком, выпрямитесь, руки вытяните вверх.',

                          'Поставьте ноги на ширину плеч, выпрямите спину.'
                          'Присед делается на вдохе. На выдохе необходимо сделать мощное выпрыгивание вверх, '
                          'оттолкнувшись полными ступнями. После того как ваши стопы полностью коснулись пола, '
                          'снова уйдите в присед.'],
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task6_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task6_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task6_do, MainGroup.Sport.Cardio.Solo.task6_help,
                    MainGroup.Sport.Cardio.Solo.task6) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                resp.response = ResponseField(
                    text=['Следующее энергичное упражнение - велосипед.',

                          'Не сдавайтесь!  На очереди упражнение под названием велосипед.'],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='997614/1ef3a8d9152694fe40e3',
                        title='Упражнение 7',
                        description='Велосипед'
                    ), buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ])
                context.set_state(MainGroup.Sport.Cardio.Solo.task7)
            else:
                resp.update({
                    'response': {
                        'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                resp.response = ResponseField(
                    text=['Лягте на спину, уберите руки за голову и разведите локти в стороны. Поочерёдно '
                          'сгибайте и выпрямляйте ноги, как будто крутите педали велосипеда, в это время '
                          'локтями касайтесь колена противоположной ноги.',

                          'Уберите руки за голову и разведите локти в стороны. Не надо складывать руки в замок или '
                          'давить ладонями на затылок — пальцы лишь слегка касаются головы. Поочерёдно сгибайте и '
                          'выпрямляйте ноги, как будто крутите педали велосипеда.'],
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task7_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task7_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task7_do, MainGroup.Sport.Cardio.Solo.task7_help,
                    MainGroup.Sport.Cardio.Solo.task7) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                resp.response = ResponseField(
                    text=['Вы молодцы, осталось совсем немного! Начинаем отжимания.',
                          'Поднажмите и выполняйте приседания.',

                          'Поднажмите и выполняйте отжимания.'],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='937455/184ba7336b4638e1442e',
                        title='Упражнение 8',
                        description='Отжимания'
                    ),
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task8)
            else:
                resp.update({
                    'response': {
                        'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                resp.response = ResponseField(
                    text=['В планке опускаем и поднимаем тело с помощью сгибания - разгибания рук от пола.',

                          'Опуститесь вниз, сгибая руки в локтевых суставах, продолжая удерживать лопатки в этом '
                          'положении и сохраняя анатомически правильные изгибы позвоночника, локти направлены '
                          'примерно под углом 45-50 градусов от туловища, затем плавно вернитесь в исходное '
                          'положение.'],
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task8_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task8_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task8_do, MainGroup.Sport.Cardio.Solo.task8_help,
                    MainGroup.Sport.Cardio.Solo.task8) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                resp.response = ResponseField(
                    text=['И наконец завершающее упражнение: делаем выпрыгивания из полувыпада.',

                          'Заканчиваем  тренировку  выпрыгиванием из полувыпадов.'],
                    card=Card(
                        type=CardType.BigImage,
                        image_id='213044/ebc7322f94861b2942e9',
                        title='Упражнение 9',
                        description='Выпрыгивания из полувыпада.'
                    ),
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='подробнее📄'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task9)
            else:
                resp.update({
                    'response': {
                        'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                resp.response = ResponseField(
                    text=['Выполнив небольшой шаг назад, опуститесь в полувыпад. Затем оттолкнитесь и в прыжке, '
                          'поднимите колено отведенной ноги до уровня грудИ. Вернитесь в полувыпад. Руки '
                          'двигаются вдоль тела как во время бег.',

                          'Встаньте прямо. Выполните прыжок с выпадом вперёд. Передняя нога – согнута в колене, '
                          'а задняя – прямая.'
                          'Приземлившись, снова выполните прыжок с выпадом с другой ноги.'],
                    buttons=[
                        Button(title='Выполнить🔥'),
                        Button(title='Пропустить⏭')
                    ]
                )
                context.set_state(MainGroup.Sport.Cardio.Solo.task9_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Solo.task9_do)
            elif state in (
                    MainGroup.Sport.Cardio.Solo.task9_do, MainGroup.Sport.Cardio.Solo.task9_help,
                    MainGroup.Sport.Cardio.Solo.task9) and (
                    'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                answer_options = [
                    'Заминка нужна, чтобы снизить до нормального уровня частоту сердечных сокращений. Хотите её выполнить?',
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
                context.set_state(MainGroup.Sport.Wrap.WarmDown.qw)
                context.update_data(callback=_finish_solo_cardio)

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

    elif state in MainGroup.Sport.Cardio.Rope:
        if state == MainGroup.Sport.Cardio.Rope.state_1:
            context.set_state(MainGroup.Sport.Wrap.WarmUp.qw)
            context.update_data(callback=_start_rope_cardio)
        elif state in (MainGroup.Sport.Cardio.Rope.start, MainGroup.Sport.Cardio.Rope.final):
            if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command:
                show_main_menu(context, resp)
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task1)
            else:
                resp.update({
                    'response': {
                        'text': 'Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение тренировки, или возвращаемся в меню?',
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task1_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Rope.task1_do)
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
                        },
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task2)
            else:
                resp.update({
                    'response': {
                        'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task2_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Rope.task2_do)
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
                        },
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task3)
            else:
                resp.update({
                    'response': {
                        'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task3_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Rope.task3_do)
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
                        },
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task4)
            else:
                resp.update({
                    'response': {
                        'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task4_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Rope.task4_do)
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
                        },
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task5)
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
                context.set_state(MainGroup.Sport.Cardio.Rope.task5_help)
            elif 'выполн' in command or 'дел' in command:
                resp.update({
                    'response': {
                        'text': f'{random.choice(MOTIVATIONS)}',
                        'tts': f'{random.choice(TRACKS_FOURTEEN)}',
                        'buttons': [
                            {
                                'title': 'Следующее упражнение▶',
                                'hide': True
                            }
                        ]
                    }
                })
                context.set_state(MainGroup.Sport.Cardio.Rope.task5_do)
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

                context.set_state(MainGroup.Sport.Wrap.WarmDown.qw)
                context.update_data(callback=finish_rope_cardio)
                # context.set_state(MainGroup.Sport.Cardio.Rope.end)
            else:
                resp.update({
                    'response': {
                        'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить упражнение", "Пропустить упражнение", "Узнать подробности"',
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
            context.set_state(MainGroup.Sport.Wrap.WarmDown.qw)
            context.update_data(callback=finish_rope_cardio)
    return resp
