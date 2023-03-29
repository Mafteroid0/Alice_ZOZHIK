import datetime
import functools
import typing

import pymorphy3
from pandas import to_timedelta

DEBUG = False

morph = pymorphy3.MorphAnalyzer(lang='ru')
TIME_UNITS = {
    'утро': 'h',
    'вечер': 'h',
    'ночь': 'h',
    'день': 'h',
    'пол': 'h',
    'час': 'h',
    'четверть': 'h',
    'минута': 'm',
}


def today() -> datetime.datetime:
    time = datetime.datetime.today()
    return time - datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second,
                                     microseconds=time.microsecond)


@functools.cache
def normalize(word: str) -> str:
    return morph.parse(word)[0].normal_form


@functools.cache
def is_real_time(text: str) -> bool:
    text = text.replace(',', '.')
    text = text.replace(';', ':')
    return text.replace(':', '').replace('.', '').isdecimal() and text.count('.') <= 1 and text.count(':') <= 1


def clean(text: str) -> str:
    for i in ('-', '.', ',', ':', '/', '\\', '|'):
        text = text.replace(i, '')
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


def parse_time(text: str) -> datetime.datetime:
    try:
        text = text.lower()
        if text.startswith('в '):
            text.removeprefix('в ')

        time = MyTime.fromdatetime(today())
        if DEBUG:
            print('t', time)

        text = text.replace('-', ':')
        if text.count(':') in (1, 2):  # Оптимизировать вызовы count
            if text.count(':') == 1:
                text = f'{text}:00'
            return time + to_timedelta(text)
        elif text.count(':') > 2:
            raise ValueError()

        # time += datetime.timedelta(hours=12)

        if text == 'час дня':
            return time + datetime.timedelta(hours=13)
        elif text == 'час ночи':
            return time + datetime.timedelta(hours=1)

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

                    time += to_timedelta(f'{word}{TIME_UNITS[txt_buf]}')
                    txt_buf = None
                    num_buf = None
                    continue

                if (not word_is_time) or txt_buf is not None:
                    if txt_buf is not None:
                        word = txt_buf

                    match word:
                        case 'полдень':
                            time = today() + datetime.timedelta(hours=12)
                            txt_buf = None
                            num_buf = None
                            continue
                        case 'полночь':
                            time = today()
                            txt_buf = None
                            num_buf = None
                            continue

                    if num_buf is None:
                        txt_buf = word
                        continue

                    time += to_timedelta(f'{num_buf}{TIME_UNITS[word]}')
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
    except BaseException as e:
        raise RuntimeError(f'Some error occurred while parsing time from text: {e}')

    return time


@functools.cache
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
    '3 часа 10 минут': today_ + datetime.timedelta(hours=3, minutes=10),
    '3 часа и 10 минут': today_ + datetime.timedelta(hours=3, minutes=10),
    '3 часа дня и 10 минут': today_ + datetime.timedelta(hours=15, minutes=10),
    'час дня': today_ + datetime.timedelta(hours=13),
    'час ночи': today_ + datetime.timedelta(hours=1),
}

for inp, excepting in time_parsing_testcases.items():
    assert (out := parse_time(inp)) == excepting, f'parse_time test failed: with input {inp} excepted output {excepting}, but got {out}'
