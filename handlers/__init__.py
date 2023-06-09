import random

from typing_ import AliceUserRequest, TrainingStep
from typing_.response import Response, \
    ResponseField, Card, CardType, Item, Button
from fsm import FSMContext
from dialogs import warm_up_algorithm, warm_down_algorithm, MOTIVATIONS, TRACKS_SIXTEEN, TRACKS_FOURTEEN, NOW_SYNONYMS

from tools import any_from

from handlers import dream, water, weight
import handlers.sport.cardio
from handlers.main_menu import show_main_menu

from states import MainGroup

from logging_ import logged, logger, DO_LOGGING


def is_positive(command: str) -> bool:
    return any_from('нач', 'готов', 'погн', 'поехали', 'давай', 'да', 'выполн', 'запус', in_=command)


def start_power_training(context: FSMContext, resp: dict | Response) -> dict | Response:
    resp.update({
        'response': {
            'text': 'Давайте приступим к силовой тренировке. Для нее Вам нужен только боевой настрой. Одно упражнение '
                    'длится 40 секунд.'
                    'Перед  его выполнением Вы можете изучить упражнение подробнее, начать делать его или пропустить '
                    'Перед  его выполнением Вы можете изучить упражнение подробнее, начать делать его или пропустить '
                    'выполнение и перейти к следующему.'
                    'Вы готовы к силовой тренировке или подберём Вам что-нибудь другое?'
                    'Вы готовы начать, или рассмотрим другую тренировку?',
            'card': {
                'type': 'ItemsList',
                'header': {
                    'text': 'Приступаем к выполнению силовой тренировки.'
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
    context.set_state(MainGroup.Sport.Power.start)
    return resp


def start_warmup(context: FSMContext, resp: dict | Response) -> dict | Response:
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
    context.set_state(MainGroup.Sport.Wrap.WarmUp.start)
    return resp


def end_warmup(context: FSMContext,
               resp: dict | Response) -> dict | Response:  # Возврат к упражнению которое было до начала разминки
    resp.update({
        'response': {
            'text': 'Вы хорошо потрудились, поздравляю вас с победой! Что выберите дальше: скажите "повторить '
                    'разминку", чтобы потренироваться ещё раз или "к тренировке", чтобы начать основную тренировку?',
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

    context.update_data(step=0)
    context.set_state(MainGroup.Sport.Wrap.WarmUp.end)

    return resp


def cancel_warmup(context: FSMContext, resp: dict | Response, data: dict | None = None) -> dict | Response:
    if data is None:
        data = context.get_data()

    return data['callback'](context, resp)


def start_session(context: FSMContext, resp: dict | Response, add_help_button: bool = True) -> dict | Response:
    # Действия при новой сессии
    answer_options = ['Привет🖐!  Всегда хотели окунуться в мир здорового образа жизни? '
                      'Поздравляю, Вы сделали правильный выбор. '
                      'Я - навык "Точка старта" помогу освоить основы ЗОЖ на практике с лёгкостью и удовольствием. '
                      'Если хотите ознакомиться с моим функционалом, то скажите "Что ты умеешь?". '
                      'Если же готовы приступить, то скажите "Поехали".',

                      'Очень приятно осознавать, что Вы решили заботится о себе и своём здоровье💖!'
                      ' Я позабочусь о Вас и облегчу ваше знакомство с ЗОЖ. Вы сможете начать следить '
                      'за Вашим здоровьем с удовольствием.'
                      ' Если нужно ознакомиться с функционалом навыка, то скажите "Что ты умеешь?". '
                      'Если уже хотите приступить, то скажите "Поехали".']
    resp.response = ResponseField(
        text=f'{random.choice(answer_options)}',
        buttons=[
            Button(title='Что ты умеешь?'),
            Button(title="Поехали!")
        ]
    )
    if add_help_button:
        resp.response.buttons.append(Button(title='Помощь', hide=False))
    context.reset_state(with_data=True)
    return resp


def start_warmdown(context: FSMContext, resp: dict | Response) -> dict | Response:
    resp.response = ResponseField(
        text='Во время тренировки Вы можете изучить упражнение подробнее, '
             'начать выполнять его или пропустить текущее упражнение и перейти к следующему.\n'
             'Вы готовы начать или выберем другую тренировку?',
        card=Card(
            type=CardType.ItemsList,
            header='Приступаем к выполнению заминки',
            items=[
                Item(title='Я готов', button='Я готов', image_id='997614/72ab6692a3db3f4e3056'),
                Item(title='Вернуться в меню', button='Вернуться в меню', image_id='1030494/cc3631c8499cdc8daf8b')
            ]
        )
    )
    context.set_state(MainGroup.Sport.Wrap.WarmDown.start)
    return resp


def end_warmdown(context: FSMContext,
                 resp: dict | Response) -> dict | Response:  # Возврат к упражнению которое было до начала разминки
    resp.response = ResponseField(
        text='Вы хорошо потрудились, поздравляю вас с  очередной победой! Что выберите дальше: '
             'скажите "повторить заминку" или "завершить заминку"?',
        card=Card(
            type=CardType.ItemsList,
            header='Повторим зазминку или перейдём к основному списку?', items=[
                Item(title='Повторить разминку', button='Повторить разминку', image_id='997614/15f977696a281092bcc0'),
                Item(title='Вернуться к основному списку', button='Назад', image_id='1030494/cc3631c8499cdc8daf8b')
            ]
        )
    )

    context.update_data(step=0)
    context.set_state(MainGroup.Sport.Wrap.WarmDown.end)

    return resp


def cancel_warmdown(context: FSMContext, resp: dict | Response, data: dict | None = None) -> dict | Response:
    if data is None:
        data = context.get_data()

    return data['callback'](context, resp)


def finish_power_training(context: FSMContext, resp: dict | Response) -> dict | Response:
    resp.update(
        dict(
            response=dict(
                text='Вы хорошо потрудились, горжусь Вами. Повторим тренировку или вернёмся в меню? Выбор за Вами.',
                card=dict(
                    type='ItemsList',
                    header={'text': 'Повторим тренировку или вернёмся в меню?'},
                    items=[
                        dict(title='Повторить тренировку', button={"text": 'Повторить тренировку'},
                             image_id='997614/15f977696a281092bcc0'),
                        dict(title='Вернуться в меню', button=dict(text='Вернуться в меню'),
                             image_id='1030494/cc3631c8499cdc8daf8b')
                    ]
                )
            )
        )
    )
    context.set_state(MainGroup.Sport.Power.final)
    return resp


@logged
def main_handler(req: AliceUserRequest, fsm: FSMContext):
    # req = AliceUserRequest(event)

    command = req.request.command

    context = fsm.build_context(req.session.user.user_id)

    state = context.get_state()

    resp = Response(version=req.version, session=req.session)

    if DO_LOGGING:
        logger.debug(f'{command=}')
        logger.debug(f'{state=}')
        logger.debug(f'{req=}')

    if req.session.new:
        start_session(context, resp)

    elif any_from(('помо', 'help'), in_=command):

        #                     buttons=context.get_data(user_id).get('buttons', None)))
        # resp = start_session(user_id, resp, add_help_button=False)
        resp.response = ResponseField(
            text=state.help_message.format(
                now=random.choice(NOW_SYNONYMS)) if state is not None else MainGroup.help_message.format(
                now=random.choice(NOW_SYNONYMS)),
            buttons=context.data.get('last_buttons', [])
        )

    elif command == 'что ты умеешь':
        answer_options = ['Очень здорово, что вы спросили меня про это. В мой функционал входит:\n'
                          '🏃‍♂️спортивные тренировки\n'
                          '😴 Фазы сна\n'
                          '🥛 Водный баланс\n'
                          '⚖ Идеальный вес\n'
                          'Чтобы перейти к списку, скажите Поехали.',

                          'Я рада, что вы решили спросить меня об этом. Если говорить вкратце, то в мой функционал '
                          'входит:\n'
                          '🏃‍♂️спортивные тренировки\n'
                          '😴 Фазы сна\n'
                          '🥛 Водный баланс\n'
                          '⚖ Идеальный вес\n'
                          'Чтобы перейти к списку, скажите "Поехали".']

        resp.update(dict(response=dict(text=f'{random.choice(answer_options)} \n', buttons=[
            dict(title='Поехали!', hide=True),
            dict(title='Помощь', hide=False)
        ])))
        context.set_state(MainGroup.main_menu)
        return resp

    elif state == MainGroup.main_menu and any_from('спорт', 'трен', in_=command) and not \
            any_from('зарядк', 'силов', 'кардио', in_=command):
        resp.response = ResponseField(
            text='Это сообщение никто не увидит :)',
            tts='Выберите одну из трёх тренировок: "Кардио", "Силовая", "Утренняя зарядка"',
            card=Card(
                type=CardType.ItemsList,
                header='Какую тренировку выберете?',
                items=[
                    Item(
                        title='кардиотренировка',
                        button='кардиотренировка',
                        description='тренировка, направленная на улучшение работы органов и укрепление эластичности сосудов',
                        image_id='1533899/13a130643a2fcdac537a'
                    ),
                    Item(
                        title='силовая тренировка',
                        button='силовая тренировка',
                        description='тренировка, направленная на укрепление мышц',
                        image_id='1533899/f030bee0ec7edea516e3'
                    ),
                    Item(
                        title='утренняя зарядка',
                        button='утренняя зарядка',
                        description='утренние упражнения для заряда бодрости',
                        image_id='1540737/cc26a14712e6995a6624'
                    ),
                    Item(
                        title='вернутсья в основное меню',
                        button='Назад',
                        description='',
                        image_id='1030494/cc3631c8499cdc8daf8b'
                    )
                ]
            )
        )
        MainGroup.Sport.state_home.set(context)

    elif state is None:
        if is_positive(command):
            show_main_menu(context, resp)
        else:
            resp.response = ResponseField(
                text='Извините, я не поняла вас. Что вы хотите сделать: "Начать" или поинтересоваться о том, '
                     'что я умею?',
                buttons=[
                    Button(title='Начать'),
                    Button(title='Что ты умеешь')
                ]
            )

    elif state in MainGroup:
        if any_from('верн', 'назад', 'основ', 'домой', 'начало', 'верш', 'конч', in_=command):
            show_main_menu(context, resp)
        elif state == MainGroup.main_menu:
            if 'вод' in command or 'баланс' in command:

                resp.response = ResponseField(
                    text=[
                        'Вода жизненно необходима каждому человеку, а употребление её дневной нормы улучшает '
                        'метаболизм. '
                        'Я подскажу, какое минимальное количество Вам необходимо выпивать в течение дня. Подскажите, '
                        'пожалуйста, Ваш вес.',

                        'Вода нужна для транспортировки питательных веществ. я расскажу, какое количество Вам нужно '
                        'выпивать в течение дня 😉\n'
                        'Подскажите, пожалуйста, Ваш вес.',

                        'Так как мы состоим из воды примерно на 70% 🐳, то употреблять её в достаточном количестве '
                        'очень'
                        'важно.\n'
                        'Не переживайте 😉 , я подскажу, какое минимальное количество Вам необходимо выпивать в течение '
                        'дня.\n'
                        'Для того, чтобы точно рассчитать минимальное объём воды, мне нужен вес человека. Подскажите, '
                        'пожалуйста, вес Вашего тела в килограммах.']
                )
                context.set_state(MainGroup.Water.state_1)

            elif 'сон' in command or 'сна' in command or 'фаз' in command:
                resp.response = ResponseField(
                    text=['Здорово, что Вы решили следить за своим сном. Подскажите, во сколько Вы хотите '
                          'проснуться, а я рассчитаю идеальное время, в которое необходимо будет лечь спать.',

                          'Сон - физиологическая потребность человека, его недостаток негативно влияет на здоровье и '
                          'продуктивность в течение дня. Подскажите, во сколько Вы хотите проснуться, а я рассчитаю '
                          'идеальное время, в которое необходимо будет лечь спать,чтобы чувствовать себя бодро в '
                          'течение всего дня.']
                )
                MainGroup.Dream.state_1.set(context)

            elif 'вес' in command:
                answer_options = [
                    'Идеальный вес -  это не только красивая фигура, но и здоровье и работоспособность. Подскажите, '
                    'пожалуйста, Ваш пол, чтобы я могла сделать точный расчёт.',
                    'Вес тела влияет на продолжительность нашей жизни. Именно поэтому так важно знать его '
                    'рекомендуемую норму. Не беспокойтесь, я рассчитаю Вашу индивидуальную рекомендацию. Подскажите '
                    'пожалуйста Ваш пол.']
                resp.update({
                    'response': {
                        'text': f'{random.choice(answer_options)}',
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

            else:
                show_main_menu(context, resp)
        elif state == MainGroup.Sport.state_home:
            if 'сил' in command:
                # answer_options = [ 'Замечательно! Кардиотренировки несут огромную пользу, а также поднимают
                # настроение. Выберите тип ' 'кардио:  классическая или со скакалкой.',
                #
                #     'Прекрасный выбор😍! Нагружая сердечно-сосудистую систему, мы укрепляем здоровье. Выберите тип '
                #     'кардио: классическая или со скакалкой.']
                resp.response = ResponseField(
                    text=[
                        'Очень хороший выбор, потому что мышечная масса способствует развитию силы и выносливости. Для большего эффекта не хотели бы Вы размяться перед основной тренировкой?',
                        'Классно, что Вы решили набрать мышечную массу! Поздравляю, потому что в скором времени у Вас обязательно будет стройное и подтянутое тело. Хотите выполнить разминку перед тренировкой?'],
                    card=Card(
                        type=CardType.ItemsList,
                        header='Хотите выполнить разминку?',
                        items=[
                            Item(title='Выполнить разминку', button='Да', image_id='213044/9c13b9b997d78cde2579'),
                            Item(title='Продолжить без разминки', button='Нет', image_id='1540737/cc47e154fc7c83b6ba0d')
                        ]
                    )
                )
                context.set_state(MainGroup.Sport.Wrap.WarmUp.qw)
                context.update_data(callback=start_power_training)

            elif 'кард' in command:
                answer_options = [
                    'Замечательно! Кардиотренировки несут огромную пользу, а также поднимают настроение. Выберите тип '
                    'кардио:  классическая или со скакалкой.',

                    'Прекрасный выбор! Нагружая сердечно-сосудистую систему, мы укрепляем здоровье. Выберите тип '
                    'кардио: классическая или со скакалкой.']
                resp.update({
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
                context.set_state(MainGroup.Sport.Cardio.state_1)

            elif 'заряд' in command:
                answer_options = [
                    'Прекрасно🔥\nДержать тело в форме необходимо всем, очень приятно, что Вы это понимаете. Однако '
                    'зарядки тоже бывают разными. Какой тип зарядки выберите: пятиминутная или десятиминутная?',
                    'Отличный выбор🤩\nЗарядка нужна всем, но немногие это понимают, к счастью к Вам это не '
                    'относится. Выберите тип зарядки: пятиминутная или десятиминутная.',
                    'Давайте вместе приведём Ваше тело в тонус. Выберите тип зарядки:  пятиминутная или десятиминутная.']
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
                context.set_state(MainGroup.Sport.Zaradka.state_1)

            elif 'верн' in command or 'назад' in command or 'меню' in command:
                show_main_menu(context, resp)

            else:
                resp.response = ResponseField(
                    text='Это сообщение никто не увидит :)',
                    tts='Не поняла вас. Выберите одну из тренировок: "Кардио", "Силовая", "Зарядка", или вернитесь в меню, чтобы выбрать другое занятие.',
                    card=Card(
                        type=CardType.ItemsList,
                        header='Какую тренировку выберете?',
                        items=[
                            Item(
                                title='кардиотренировка',
                                button='кардиотренировка',
                                description='тренировка, направленная на улучшение работы органов и укрепление эластичности сосудов',
                                image_id='1533899/13a130643a2fcdac537a'
                            ),
                            Item(
                                title='силовая тренировка',
                                button='силовая тренировка',
                                description='тренировка, направленная на укрепление мышц',
                                image_id='1533899/f030bee0ec7edea516e3'
                            ),
                            Item(
                                title='утренняя зарядка',
                                button='утренняя зарядка',
                                description='утренние упражнения для заряда бодрости',
                                image_id='1540737/cc26a14712e6995a6624'
                            ),
                            Item(
                                title='вернутсья в основное меню',
                                button='Назад',
                                description='',
                                image_id='1030494/cc3631c8499cdc8daf8b'
                            )
                        ]
                    )
                )
                MainGroup.Sport.state_home.set(context)
        elif state in MainGroup.Dream:
            dream.dream_handler(context, req, resp)
        elif state in MainGroup.Water:
            water.water_handler(context, req, resp)
        elif state in MainGroup.Weight:
            weight.weight_handler(context, req, resp)

        elif state in MainGroup.Sport.Cardio:
            handlers.sport.cardio.cardio_handler(context, req, resp)

        elif state in MainGroup.Sport.Zaradka:
            if state == MainGroup.Sport.Zaradka.state_1:
                if 'пят' in command or '5' in command:
                    resp.update({
                        'response': {
                            'text': 'Приготовьтесь получить заряд бодрости! Каждое упражнение длится минуту.Перед '
                                    'выполнением каждого упражнения Вы можете изучить его подробнее, '
                                    'начать выполнение или пропустить его и перейти к следующему.'
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
                    context.set_state(MainGroup.Sport.Zaradka.Five.start)
                elif 'дес' in command or '10' in command:
                    resp.update({
                        'response': {
                            'text': 'Итак, начинаем нашу активную 10-минутную зарядку. Надеюсь Вы полны энтузиазма. '
                                    'Каждое упражнение длится 60 секунд.\n'
                                    'Перед выполнением каждого упражнения Вы можете изучить его подробнее, '
                                    'начать выполнение или пропустить его и перейти к следующему. Вы готовы начать '
                                    'или подберём другую тренировку?',
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
                    context.set_state(MainGroup.Sport.Zaradka.Ten.start)
                else:
                    resp.update({
                        'response': {
                            'text': 'Уточните, пожалуйста, Вы собираетесь выполнить пятиминутную или десятиминутную '
                                    'тренировку?',
                            'buttons': [
                                {
                                    'title': 'Пятиминутная',
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
                    if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command or 'верш' in command or 'конч' in command:
                        show_main_menu(context, resp)
                    elif is_positive(command):
                        resp.update({
                            'response': {
                                'text': 'Приступаем  к растиранию шеи!',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/187806e12d9cfa5a2e7b',
                                    "title": 'Упражнение 1',
                                    "description": 'Растирание шеи'
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task1)
                    else:
                        resp.update(
                            dict(
                                response=dict(
                                    text='Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение '
                                         'тренировки, или возвращаемся в меню?',
                                    buttons=[
                                        dict(title='Вернуться в меню', hide=True),
                                        dict(title='Запустить тренировку', hide=True)
                                    ]
                                )
                            )
                        )
                elif state in (
                        MainGroup.Sport.Zaradka.Ten.task1, MainGroup.Sport.Zaradka.Ten.task1_help,
                        MainGroup.Sport.Zaradka.Ten.task1_do) or (
                        state == MainGroup.Sport.Zaradka.Ten.final and 'повтор' in command):
                    if 'подробн' in command or 'объяс' in command:
                        resp.update({
                            'response': {
                                'text': 'Начинаем поглаживания тыльной стороны шеи обеими руками. Их необходимо '
                                        'прижимать ладонями к массируемой части. Перемещаемся от границы волосяного '
                                        'покрова до плечевого сустава.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task1_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task1_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task2)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'Плавно наклоняйте голову к правому, а затем к левому плечу. Рекомендую '
                                        'делать упражнение как можно медленнее.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task2_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task2_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task3)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'Ладони разжаты. Удерживая плечи и предплечья неподвижными, вращение '
                                        'осуществляется только кистями.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task3_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task3_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task4)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'Не отрывая ног от пола, начинаем наклонять тело в правую, а затем в левую '
                                        'сторону, руки лучше держать на поясе.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task4_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task4_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task5)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'Встаньте прямо и вытяните руки по сторонам. Тело образует букву «Т». Это '
                                        'исходное положение. Выполняйте круговые движения прямыми руками вперёд, '
                                        'затем – назад.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task5_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task5_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task6)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'Положите руки на талию, ноги расставьте шире плеч. Начните вращать тазом по '
                                        'кругу, как будто стараетесь нарисовать круг ягодицами. Стопы не отрываются '
                                        'от пола, вращение происходит за счет движений таза, а не корпуса.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task6_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task6_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task7)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'В планке опускаем и поднимаем тело с помощью сгибания - разгибания рук от '
                                        'пола.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task7_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task7_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task8)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'По сути это обычный бег, но без передвижения. Спину необходимо держать '
                                        'максимально ровно; руки согнуть в локтях, не задирая и не расслабляя их '
                                        'слишком сильно',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task8_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task8_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task9)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'Ноги на ширине плеч, спина прямая, лопатки сведены, руки подняты к ушам. '
                                        'Напрягите пресс и наклоняйтесь вниз. Постарайтесь тянуться грудью к бедрам, '
                                        'а не руками к полу.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task9_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task9_do)
                    elif state in (
                            MainGroup.Sport.Zaradka.Ten.task9_do, MainGroup.Sport.Zaradka.Ten.task9_help,
                            MainGroup.Sport.Zaradka.Ten.task9) and (
                            'проп' in command or 'след' in command or 'прод' in command or 'дал' in command):
                        resp.update({
                            'response': {
                                'text': 'Наращиваем интенсивность. Не беспокойтесь, делаем классические приседания.',
                                'card': {
                                    'type': 'BigImage',
                                    "image_id": '1540737/8c6ed8b8b2ea3d6c636d',
                                    "title": 'Упражнение 10',
                                    "description": 'Приседания'
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task10)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                                'text': 'Чтобы выполнить стандартное приседание, нужно держать спину прямо. После чего начните медленно опускать бедра, пока они не станут параллельны полу.',
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task10_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Ten.task10_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Ten.final)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Не совсем понимаю о чём вы. Сейчас доступны следующие команды:\n"Выполнить '
                                        'упражнение", "Пропустить упражнение", "Узнать подробности"',
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
                    if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command or 'верш' in command or 'конч' in command:
                        show_main_menu(context, resp)
                    elif is_positive(command):
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task1)
                    else:
                        resp.update({
                            'response': {
                                'text': 'Извините, не поняла вас. Пожалуйста, уточните: Мы начинаем выполнение '
                                        'тренировки, или возвращаемся в меню?'
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task1_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Five.task1_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task2)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task2_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Five.task2_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task3)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task3_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Five.task3_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task4)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task4_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Five.task4_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task5)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.task5_help)
                    elif 'выполн' in command or 'дел' in command:
                        resp.update({
                            'response': {
                                'text': f'{random.choice(MOTIVATIONS)}',
                                'tts': f'{random.choice(TRACKS_SIXTEEN)}',
                                'buttons': [
                                    {
                                        'title': 'Следующее упражнение▶',
                                        'hide': True
                                    }
                                ]
                            }
                        })
                        context.set_state(MainGroup.Sport.Zaradka.Five.task5_do)
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
                        context.set_state(MainGroup.Sport.Zaradka.Five.final)
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
                if 'друг' in command or 'не' in command or 'меню' in command or 'верн' in command or 'верш' in command or 'конч' in command:
                    show_main_menu(context, resp)
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
                    context.set_state(MainGroup.Sport.Power.task1)
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
                    context.set_state(MainGroup.Sport.Power.task1_help)
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
                    context.set_state(MainGroup.Sport.Power.task1_do)
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
                    context.set_state(MainGroup.Sport.Power.task2)
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
                    context.set_state(MainGroup.Sport.Power.task2_help)
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
                    context.set_state(MainGroup.Sport.Power.task2_do)
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
                    context.set_state(MainGroup.Sport.Power.task3)
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
                    context.set_state(MainGroup.Sport.Power.task3_help)
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
                    context.set_state(MainGroup.Sport.Power.task3_do)
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
                    context.set_state(MainGroup.Sport.Power.task4)
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
                    context.set_state(MainGroup.Sport.Power.task4_help)
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
                    context.set_state(MainGroup.Sport.Power.task4_do)
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
                    context.set_state(MainGroup.Sport.Power.task5)
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
                    context.set_state(MainGroup.Sport.Power.task5_help)
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
                    context.set_state(MainGroup.Sport.Power.task5_do)
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
                    context.set_state(MainGroup.Sport.Power.task6)
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
                    context.set_state(MainGroup.Sport.Power.task6_help)
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
                    context.set_state(MainGroup.Sport.Power.task6_do)
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
                    context.set_state(MainGroup.Sport.Power.task7)
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
                    context.set_state(MainGroup.Sport.Power.task7_help)
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
                    context.set_state(MainGroup.Sport.Power.task7_do)
                elif (state in (
                        MainGroup.Sport.Power.task7_do, MainGroup.Sport.Power.task7_help,
                        MainGroup.Sport.Power.task7) and (
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
                    context.set_state(MainGroup.Sport.Wrap.WarmDown.qw)
                    context.update_data(callback=finish_power_training)
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

                context.set_state(MainGroup.Sport.Power.end)

        elif state in MainGroup.Sport.Wrap.WarmUp:
            step: TrainingStep = warm_up_algorithm[context.get_data().get('step', 0)]

            if state == MainGroup.Sport.Wrap.WarmUp.qw:
                if 'нет' in command or 'не ' in command:
                    resp = cancel_warmup(context, resp)
                elif 'да' in command or 'конечн' in command:
                    resp = start_warmup(context, resp)
                else:
                    resp.update({
                        'response': {
                            'text': 'Извините, кажется я прослушала😣\nВы хотите выполнить разминку?',
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
                context.set_state(MainGroup.Sport.Wrap.WarmUp.task)
                step: int = 0
                context.update_data(step=step)

                step: TrainingStep = warm_up_algorithm[step]

                resp.update(step.generate_choice_resp())

            elif 'подробн' in command or 'расскажи' in command:
                resp.update(step.generate_detailed_description_resp())

            elif is_positive(command):
                resp = step.generate_do_training_resp(random.choice(MOTIVATIONS), random.choice(TRACKS_FOURTEEN))

            elif state == MainGroup.Sport.Wrap.WarmUp.end:
                if 'повтор' in command or 'ещё' in command or 'еще' in command or 'снов' in command:
                    resp = start_warmup(context, resp)

                elif 'трен' in command or 'пере' in command or 'закон' in command:
                    cancel_warmup(context, resp)
                else:
                    resp.update({
                        'response': {
                            'text': 'Извините, не поняла вас. Сейчас доступны следующие команды:\n"Повторить  разминку", "Перейти к тренировке".',
                            'buttons': [
                                {
                                    'title': 'Повторить разминку',
                                    'hide': True
                                },
                                {
                                    'title': 'Перейти к тренировке',
                                    'hide': True
                                }
                            ]

                        }
                    })

            elif 'пропуст' in command or 'следующ' in command or 'дальш' in command or 'продолж' in command:
                if state == MainGroup.Sport.Wrap.WarmUp.task:
                    step = context.get_data().get('step', 0) + 1
                    context.update_data(step=step)

                    try:
                        step: TrainingStep = warm_up_algorithm[step]
                    except IndexError:
                        end_warmup(context, resp)
                    else:
                        resp.update(step.generate_choice_resp())

                elif state == MainGroup.Sport.Wrap.WarmUp.start:
                    cancel_warmup(context, resp)

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

        elif state in MainGroup.Sport.Wrap.WarmDown:
            step: TrainingStep = warm_down_algorithm[context.get_data().get('step', 0)]

            if state == MainGroup.Sport.Wrap.WarmDown.qw:
                if 'нет' in command or 'не ' in command or 'без' in command:
                    resp = cancel_warmdown(context, resp)
                elif is_positive(command):
                    resp = start_warmdown(context, resp)
                else:
                    resp.update({
                        'response': {
                            'text': 'Извините, кажется я прослушала😣\nВы хотите выполнить заминку?',
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

            elif state == MainGroup.Sport.Wrap.WarmDown.start:
                if is_positive(command):
                    context.set_state(MainGroup.Sport.Wrap.WarmDown.task)
                    step: int = 0
                    context.update_data(step=step)

                    step: TrainingStep = warm_down_algorithm[step]

                    resp.update(step.generate_choice_resp())
                else:
                    resp.update({
                        'response': {
                            'text': 'Не совсем поняла вас. Прямо сейчас Вы можете начать выполнение, сказав "Готов" или "Вернуться в меню" и выбрать другое занятие',
                            'buttons': [
                                {
                                    'title': 'Готов',
                                    'hide': True
                                },
                                {
                                    'title': 'Вернуться в меню',
                                    'hide': True
                                }
                            ]

                        }
                    })

            elif 'подробн' in command or 'расскажи' in command:
                resp.update(step.generate_detailed_description_resp())

            elif is_positive(command):
                resp.update(step.generate_do_training_resp(random.choice(MOTIVATIONS), random.choice(TRACKS_FOURTEEN)))

            elif state == MainGroup.Sport.Wrap.WarmDown.end:
                if 'повтор' in command or 'ещё' in command or 'еще' in command or 'снов' in command:
                    resp = start_warmdown(context, resp)
                else:
                    cancel_warmdown(context, resp)

            elif 'пропуст' in command or 'следующ' in command or 'дальш' in command or 'продолж' in command:
                if state == MainGroup.Sport.Wrap.WarmDown.task:
                    step = context.get_data().get('step', 0) + 1
                    context.update_data(step=step)

                    try:
                        step: TrainingStep = warm_down_algorithm[step]
                    except IndexError:
                        end_warmdown(context, resp)
                    else:
                        resp.update(step.generate_choice_resp())

                elif state == MainGroup.Sport.Wrap.WarmDown.start:
                    cancel_warmdown(context, resp)

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

        elif is_positive(command):
            show_main_menu(context, resp)

    else:
        resp.update({
            'response': {
                'text': f'Произошла ошибка. Скажите "Поехали" чтобы вернуться в главное меню.'
            }
        })
        context.set_state(MainGroup.main_menu)

    if resp.get('response', None) is None:
        resp['response'] = {
            'text': f'Не совсем поняла вас. {state.help_message.format(now=random.choice(NOW_SYNONYMS))}'}
    response = resp['response']
    if not (buttons := response.get('buttons', [])):
        response['buttons'] = buttons

    for button in buttons:
        if button.get('title', '').lower() == 'помощь':
            break
    else:
        buttons.append({'title': 'Помощь', 'hide': False})
    context.update_data(last_buttons=buttons)

    return resp
