from fsm import FSMContext, StatesGroup, State

fsm = FSMContext()


class MainGroup(StatesGroup):  # Состояние по умолчанию это None, его не нужно явно определять
    _fsm = fsm
    _help_message = '{now} Вам доступны следующие команды: "Поехали" (чтобы перейти к выбору тренировки или расчёту ' \
                    'информации) и "Что ты умеешь?" (для уточнения моего функционала)'
    _default_state = None

    state_1 = State(_help_message = '{now} Вы можете выбрать себе занятие из предоставленного списка: "Спортивные тренировки", "Водный баланс", "Фазы сна", "Идевльный вес"')

    class Water(StatesGroup):
        _help_message = '{now} Вы можете "Вернуться к основному списку", то есть в меню, или "Рассчитать ещё раз" и ' \
                        'воспользоваться этой функцией повторно.'

        state_1 = State(_help_message='Сейчас вам следует ввести свой вес.')
        end = State(
            _help_message='{now} Вы можете ещё раз выполнить вычисление, или "Вернуться к основному списку", то есть в меню.')

    class Dream(StatesGroup):
        _help_message = '{now} Вы можете "Вернуться к основному списку", то есть в меню, или "Рассчитать ещё раз" и ' \
                        'воспользоваться этой функцией повторно.'

        state_1 = State()
        end = State(
            _help_message='{now} Вы можете ещё раз выполнить вычисление, или "Вернуться к основному списку", то есть в меню.'
        )

    class Weight(StatesGroup):
        _help_message = '{now} Вы можете ввести свой пол, чтобы продолжить вычисление, или "Вернуться к основному списку", ' \
                        'то есть в меню.'

        state_1 = State(_help_message = '{now} Вы можете ввести свой пол, чтобы продолжить вычисление, или "Вернуться к основному списку", ' \
                        'то есть в меню.')
        sex_choose = State(_help_message='Сейчас вам следует ввести свой рост')
        end = State(
            _help_message='{now} Вы можете ещё раз выполнить вычисление, или "Вернуться к основному списку", то есть в меню.'
        )

    class Sport(StatesGroup):
        qw = State()

        _help_message = '{now} Вам доступны команды: "Подробнее" (чтобы узнать правильную технику выполнения), "Выполнить ' \
                        'упражнение" (чтобы начать тренироваться) и "Пропустить упражнение" (чтобы перейти к ' \
                        'следующему упражнению в текущей тренировке)'

        class Wrap(StatesGroup):
            _help_message = ''

            class WarmUp(StatesGroup):
                _help_message = ''

                qw = State(
                    _help_message='{now} Вы можете перейти к разминке командой "Да". Также вы можете пропустить разминку '
                                  'командой "Нет"'
                )
                start = State(
                    _help_message='{now} Вы можете перейти к разминке командой "Да". Также вы можете пропустить разминку '
                                  'командой "Пропустить"'
                )

                task = State()

                end = State()

            class WarmDown(StatesGroup):
                _help_message = ''

                qw = State(
                    _help_message='{now} Вы можете перейти к заминке командой "Поехали". Также можно вернуться '
                                  'обратно к'
                                  'выбору тренировки командой "Вернуться к основному списку"'
                )
                start = State(
                    _help_message='{now} Вы можете перейти к заминке командой "Поехали". Также можно вернуться '
                                  'обратно к'
                                  'выбору тренировки командой "Вернуться к основному списку"'
                )

                task = State()

                end = State()

        state_home = State(_help_message='Выберите одну из тренировок: "кардио", "силовая", "Утренняя зарядка", или произнесите "вернуться", чтобы попасть в главное меню.')

        class Power(StatesGroup):
            _help_message = ''

            state_1 = State(
                _help_message='{now} Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также можно '
                              'вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
            )
            start = State(
                _help_message='{now} Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также можно '
                              'вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
            )
            task1 = State()
            task1_help = State()
            task1_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
            task2 = State()
            task2_help = State()
            task2_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
            task3 = State()
            task3_help = State()
            task3_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
            task4 = State()
            task4_help = State()
            task4_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
            task5 = State()
            task5_help = State()
            task5_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
            task6 = State()
            task6_help = State()
            task6_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
            task7 = State()
            task7_help = State()
            task7_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
            task8 = State()
            task8_help = State()
            task8_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
            end = State()
            final = State()

        class Cardio(StatesGroup):
            _help_message = '{now} Вас есть выбор между классической (вызывается командой "классическая") и тренировкой с ' \
                            'дополнительным инвентарём в виде скакалки (команда - "Со скакалкой")'

            state_1 = State(
                _help_message='{now} У Вас есть выбор между классической (вызывается командой "классическая") и тренировкой '
                              'с дополнительным инвентарём в виде скакалки (команда - "Со скакалкой")'
            )

            class Solo(StatesGroup):
                _help_message = ''

                state_1 = State(
                    _help_message='{now} Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
                start = State(
                    _help_message='{now} Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
                task1 = State()
                task1_help = State()
                task1_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task2 = State()
                task2_help = State()
                task2_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task3 = State()
                task3_help = State()
                task3_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task4 = State()
                task4_help = State()
                task4_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task5 = State()
                task5_help = State()
                task5_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task6 = State()
                task6_help = State()
                task6_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task7 = State()
                task7_help = State()
                task7_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task8 = State()
                task8_help = State()
                task8_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task9 = State()
                task9_help = State()
                task9_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                final = State(_help_message='{now} Вы можете "Повторить тренировку" или "Завершить тренировку"')

            class Rope(StatesGroup):
                _help_message='{now} Вы можете перейти к выполнению упражнения командой "Выполнить", узнать об упражнении "подробнее", или "пропустить" выполнение'

                state_1 = State(
                    _help_message='{now} Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
                start = State(
                )
                task1 = State()
                task1_help = State()
                task1_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task2 = State()
                task2_help = State()
                task2_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task3 = State()
                task3_help = State()
                task3_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task4 = State()
                task4_help = State()
                task4_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task5 = State()
                task5_help = State()
                task5_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                end = State()
                final = State(_help_message='{now} Вы можете "Повторить тренировку" или "Завершить тренировку"')

        class Zaradka(StatesGroup):
            _help_message = ''

            state_1 = State(_help_message='используйте одну из команд "пятиминутная" или "десятиминутная";')

            class Five(StatesGroup):
                _help_message='{now} Вы можете перейти к выполнению упражнения командой "Выполнить", узнать об упражнении "подробнее", или "пропустить" выполнение'

                start = State(
                    _help_message='{now} Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
                task1 = State()
                task1_help = State()
                task1_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task2 = State()
                task2_help = State()
                task2_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task3 = State()
                task3_help = State()
                task3_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task4 = State()
                task4_help = State()
                task4_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task5 = State()
                task5_help = State()
                task5_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                end = State()
                final = State(_help_message='{now} Вы можете "Повторить тренировку" или "Завершить тренировку"')

            class Ten(StatesGroup):
                _help_message = ''

                start = State(
                    _help_message='{now} Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1 = State(
                    _help_message='{now} Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1_help = State()
                task1_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task2 = State()
                task2_help = State()
                task2_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task3 = State()
                task3_help = State()
                task3_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task4 = State()
                task4_help = State()
                task4_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task5 = State()
                task5_help = State()
                task5_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task6 = State()
                task6_help = State()
                task6_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task7 = State()
                task7_help = State()
                task7_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task8 = State()
                task8_help = State()
                task8_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task9 = State()
                task9_help = State()
                task9_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                task10 = State()
                task10_help = State()
                task10_do = State(_help_message='{now} Вы можете перейти к следующему упражнению, попросив меня об этом.')
                end = State()
                final = State(_help_message='{now} Вы можете "Повторить тренировку" или "Завершить тренировку"')
