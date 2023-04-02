from fsm import FSMContext, StatesGroup, State

fsm = FSMContext()


class MainGroup(StatesGroup):  # Состояние по умолчанию это None, его не нужно явно определять
    _fsm = fsm
    _help_message = 'Вам доступны следующие команды: "Поехали" (чтобы перейти к выбору тренировки или расчёту ' \
                    'информации) и "Что ты умеешь?" (для уточнения моего функционала)'
    _default_state = None

    state_1 = State()

    class Water(StatesGroup):
        _help_message = 'Вы можете "Вернуться к основному списку", то есть в меню, или "Рассчитать ещё раз" и ' \
                        'воспользоваться этой функцией повторно.'

        state_1 = State()
        end = State()

    class Dream(StatesGroup):
        _help_message = 'Вы можете "Вернуться к основному списку", то есть в меню, или "Рассчитать ещё раз" и ' \
                        'воспользоваться этой функцией повторно.'

        state_1 = State()
        end = State()

    class Sport(StatesGroup):
        qw = State()

        _help_message = 'Вам доступны команды: "Подробнее" (чтобы узнать правильную технику выполнения), "Выполнить ' \
                        'упражнение" (чтобы начать тренироваться) и "Пропустить упражнение" (чтобы перейти к ' \
                        'следующему упражнению в текущей тренировке)'

        class Wrap(StatesGroup):
            _help_message = ''

            class WarmUp(StatesGroup):
                _help_message = ''

                qw = State(
                    _help_message='Вы можете перейти к разминке командой "Да". Также вы можете пропустить разминку '
                                  'командой "Нет"'
                )
                start = State(
                    _help_message='Вы можете перейти к разминке командой "Да". Также вы можете пропустить разминку '
                                  'командой "Пропустить"'
                )

                task = State()

                end = State()

            class WarmDown(StatesGroup):
                _help_message = ''

                qw = State(
                    _help_message='Вы можете перейти к заминке командой "Поехали". Также можно вернуться обратно к '
                                  'выбору тренировки командой "Вернуться к основному списку"'
                )
                start = State(
                    _help_message='Вы можете перейти к заминке командой "Поехали". Также можно вернуться обратно к '
                                  'выбору тренировки командой "Вернуться к основному списку"'
                )

                task = State()

                end = State()

        state_home = State(_help_message='произнесите названеие занятия из приведённого списка, чтобы перейти к нему')

        class Power(StatesGroup):
            _help_message = ''

            state_1 = State(
                _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также можно '
                              'вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
            )
            start = State(
                _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также можно '
                              'вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
            )
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
            _help_message = 'Вас есть выбор между классической (вызывается командой "классическая") и тренировкой с ' \
                            'дополнительным инвентарём в виде скакалки (команда - "Со скакалкой")'

            state_1 = State(
                _help_message='У Вас есть выбор между классической (вызывается командой "классическая") и тренировкой '
                              'с дополнительным инвентарём в виде скакалки (команда - "Со скакалкой")'
            )

            class Solo(StatesGroup):
                _help_message = ''

                state_1 = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
                start = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
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
                    _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
                start = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
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
                    _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
                task1 = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также '
                                  'можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"'
                )
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
                    _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
                task1 = State(
                    _help_message='Вы можете перейти к выполнению упражнения командой "Запустить тренировку". Также можно вернуться обратно к выбору тренировки командой "Вернуться к основному списку"')
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
