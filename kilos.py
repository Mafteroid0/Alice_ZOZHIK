import datetime

import pymorphy2
from pandas import to_timedelta

morph = pymorphy2.MorphAnalyzer(lang='ru')
TIME_UNITS = {
    'утро': 'h',
    'вечер': 'h',
    'ночь': 'h',
    'день': 'h',
}


def today() -> datetime.datetime:
    time = datetime.datetime.today()
    return time - datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second, microseconds=time.microsecond)


def normalize(word: str) -> str:
    return morph.parse(word)[0].normal_form


def is_real_time(text: str) -> bool:
    text = text.replace(',', '.')
    text = text.replace(';', ':')
    return text.replace(':', '').replace('.', '').isdecimal() and text.count('.') <= 1 and text.count(':') <= 1


def parse_time(text: str) -> datetime.datetime:
    text_l = text.split()

    time = today()

    num_buf: str | None = None
    txt_buf: str | None = None
    minus_one: bool = False  # Надел на парсинг "Половина четвёртого"
    for word_is_time, word in map(lambda x: (is_real_time(x), x), text_l):
        if not word_is_time:
            word = normalize(word).lower()
            match word:
                case 'вечер' | 'день':
                    time += datetime.timedelta(hours=12)
                case 'час':
                    continue

        if word_is_time or num_buf is not None and txt_buf is not None:
            if num_buf is not None:
                word = num_buf

            if txt_buf is None:
                num_buf = word
                continue

            time += to_timedelta(word, unit=TIME_UNITS[normalize(txt_buf)])
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

    if time == today():
        time += datetime.timedelta(hours=int(num_buf))  # TODO: Опасное место, может вызывать много ошибок. Нужно проработать

    return time


print(parse_time('4'))
