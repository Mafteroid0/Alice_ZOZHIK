import datetime
import functools
import typing

import pymorphy3
# from pandas import to_timedelta

from logging_ import logged, logger

DEBUG = False

morph = pymorphy3.MorphAnalyzer(lang='ru')
TIME_UNITS = {
    'утро': 'hours',
    'вечер': 'hours',
    'ночь': 'hours',
    'день': 'hours',
    'пол': 'hours',
    'час': 'hours',
    'четверть': 'hours',
    'минута': 'minutes',
}


def today(hours: int = 0, minutes: int = 0, seconds: int = 0, microseconds: int = 0) -> datetime.datetime:
    time = datetime.datetime.today()
    return time - datetime.timedelta(hours=time.hour - hours, minutes=time.minute - minutes,
                                     seconds=time.second - seconds,
                                     microseconds=time.microsecond - microseconds)


@functools.cache
@logged
def normalize(word: str) -> str:
    return morph.parse(word)[0].normal_form


@functools.cache
@logged
def is_real_time(text: str) -> bool:
    text = text.replace(',', '.')
    text = text.replace(';', ':')
    return text.replace(':', '').replace('.', '').isdecimal() and text.count('.') <= 1 and text.count(':') <= 1


def clean(text: str) -> str:
    for i in ('.', ',', ':', '/', '\\', '|'):
        text = text.replace(i, '')
    text.replace('-', ' ')
    return text


class MyTime(datetime.datetime):
    @classmethod
    def fromdatetime(cls, dt: datetime.datetime):
        return cls.fromtimestamp(dt.timestamp())

    def __add__(self, other):
        if DEBUG:
            print('+', other)
        return super().__add__(other)

    def __sub__(self, other):
        if DEBUG:
            print('-', other)
        return super().__sub__(other)


@logged
def parse_time(text: str) -> datetime.datetime:
    try:
        text = text.lower()
        if text.startswith('в '):
            text = text.removeprefix('в ')
        text = text.replace('всем', '7')

        time = MyTime.fromdatetime(today())
        if DEBUG:
            print('t', time)

        text = text.replace('-', ':')
        if text.count(':') in (1, 2):  # Оптимизировать вызовы count
            if text.count(':') == 1:
                text = f'{text}:00'
            time = datetime.datetime.strptime(text, '%X')
            return today(time.hour, time.minute, time.second, time.microsecond)
        elif text.count(':') > 2:
            raise ValueError()

        # time += datetime.timedelta(hours=12)

        if text == 'час дня':
            return time + datetime.timedelta(hours=13)
        elif text == 'час ночи':
            return time + datetime.timedelta(hours=1)
        elif text == '12 ночи':
            return time

        temp = [[]]
        index = 0
        for word in clean(text).split():
            if word == 'и':
                index += 1
                try:
                    temp[index]
                except IndexError:
                    temp.append([])
                continue
            temp[index].append(word)

        del index

        for text_l in temp:
            parsed: list[str] = []

            num_buf: str | None = None
            txt_buf: str | None = None
            for word_is_time, word in map(lambda x: (is_real_time(x), x), text_l):
                parsed.append(normalize(word))
                if not word_is_time:
                    word = normalize(word)
                    match word:
                        case 'вечер' | 'день':
                            time += datetime.timedelta(hours=12)
                        case 'пол':
                            time -= datetime.timedelta(minutes=30)
                        case 'четверть':
                            time -= datetime.timedelta(minutes=45)

                if word_is_time or num_buf is not None and txt_buf is not None:
                    if txt_buf is None:
                        num_buf = word
                        continue

                    time += datetime.timedelta(**{f'{TIME_UNITS[txt_buf]}': float(word) if '.' in word else int(word)})
                    txt_buf = None
                    num_buf = None
                    continue

                if (not word_is_time) or txt_buf is not None:
                    if txt_buf is not None:
                        word = txt_buf

                    if word == 'полдень':
                        time = today() + datetime.timedelta(hours=12)
                        txt_buf = None
                        num_buf = None
                        continue
                    elif word == 'полночь':
                        time = today()
                        txt_buf = None
                        num_buf = None
                        continue

                    elif num_buf is None:
                        txt_buf = word
                        continue

                    time += datetime.timedelta(
                        **{f'{TIME_UNITS[word]}': float(num_buf) if '.' in num_buf else int(num_buf)})
                    txt_buf = None
                    num_buf = None
                    continue

            # Тут хендлим всё, что не попадает под модель "число указатель" или "указатель число"

            if time == today() and num_buf is not None:
                num_buf: int = int(num_buf)  # TODO: Опасное место, может правоцировать много ошибок. Нужно проработать
                time += datetime.timedelta(
                    hours=num_buf)

            if time.hour in (12, 0) and time.day == today().day + 1:
                time -= datetime.timedelta(hours=12)

            if time == today() and text != 'полночь':
                if text == 'полдень':
                    time += datetime.timedelta(hours=12)
                else:
                    raise ValueError(f'Невозможно распарсить текст: {text}')

    except BaseException as e:
        raise RuntimeError(f'Some error occurred while parsing time from text: {e}')

    return time


# @functools.cache
@logged
def iter_go_sleep_time(wake_up_time: datetime.datetime, limit: int = 6) -> typing.Iterator[datetime.datetime]:
    first_go_sleep_time = wake_up_time - datetime.timedelta(minutes=(limit + 1) * 90 + 15)
    print(f'{wake_up_time=}')
    print(f'{first_go_sleep_time=}')
    print(f'{limit=}')
    for i in range(limit):
        print(f'{first_go_sleep_time + datetime.timedelta(minutes=(i + 1) * 90)=}')
        yield first_go_sleep_time + datetime.timedelta(minutes=(i + 1) * 90)


today_ = today()

time_parsing_testcases = {
    'Полдень': today_ + datetime.timedelta(hours=12),
    'Полночь': today_,
    '7 утра': today_ + datetime.timedelta(hours=7),
    '7 часов утра': today_ + datetime.timedelta(hours=7),
    '3 ночи': today_ + datetime.timedelta(hours=3),
    '3 дня': today_ + datetime.timedelta(hours=15),
    'пол 3': today_ + datetime.timedelta(hours=2, minutes=30),
    'четверть 3': today_ + datetime.timedelta(hours=2, minutes=15),
    '3': today_ + datetime.timedelta(hours=3),
    '12:32': today_ + datetime.timedelta(hours=12, minutes=32),
    '12-32': today_ + datetime.timedelta(hours=12, minutes=32),
    '12:00': today_ + datetime.timedelta(hours=12),
    '7:00': today_ + datetime.timedelta(hours=7),
    '3 часа 10 минут': today_ + datetime.timedelta(hours=3, minutes=10),
    '3 часа и 10 минут': today_ + datetime.timedelta(hours=3, minutes=10),
    '3 часа дня и 10 минут': today_ + datetime.timedelta(hours=15, minutes=10),
    'час дня': today_ + datetime.timedelta(hours=13),
    'час ночи': today_ + datetime.timedelta(hours=1),
    'всем': today_ + datetime.timedelta(hours=7)
}

for inp, excepting in time_parsing_testcases.items():
    assert (out := parse_time(
        inp)) == excepting, f'parse_time test failed: with input {inp} excepted output {excepting}, but got {out}'
