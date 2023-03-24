import datetime
import functools

import pymorphy2
from pandas import to_timedelta

morph = pymorphy2.MorphAnalyzer(lang='ru')
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
    for i in ('-', '.', ',', ':'):
        text = text.replace(i, '')
    return text.lower()


def parse_time(text: str) -> datetime.datetime:
    time = today()

    text = text.replace('-', ':')
    if text.count(':') in (1, 2):  # Оптимизировать вызовы count
        if text.count(':') == 1:
            text = f'{text}:00'
        return time + to_timedelta(text)
    elif text.count(':') > 2:
        raise ValueError()

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
            print(1)
            if not word_is_time:
                print(2)
                word = normalize(word)
                match word:
                    case 'ночь' | 'утро':
                        if 'пол' in parsed or 'четверть' in parsed:
                            print('1-', datetime.timedelta(hours=12))
                            time -= datetime.timedelta(hours=12)
                    case 'вечер' | 'день':
                        if not ('пол' in parsed or 'четверть' in parsed):
                            print('2+', datetime.timedelta(hours=12))
                            time += datetime.timedelta(hours=12)
                    case 'пол':
                        print('3-', datetime.timedelta(minutes=30))
                        time -= datetime.timedelta(minutes=30)
                        print('4+', datetime.timedelta(hours=12))
                        time += datetime.timedelta(hours=12)
                    case 'четверть':
                        print('5-', datetime.timedelta(minutes=45))
                        time -= datetime.timedelta(minutes=45)
                        print('6+', datetime.timedelta(hours=12))
                        time += datetime.timedelta(hours=12)

            print([*parsed, txt_buf])
            if 'минута' in [*parsed, txt_buf] and int(num_buf) < 12:
                print('6.1+', datetime.timedelta(hours=12))
                time += datetime.timedelta(hours=12)

            if word_is_time or num_buf is not None and txt_buf is not None:
                if txt_buf is None:
                    num_buf = word
                    continue

                print('7+', to_timedelta(f'{word}{TIME_UNITS[txt_buf]}'))
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

                print('8+', to_timedelta(f'{num_buf}{TIME_UNITS[word]}'))
                time += to_timedelta(f'{num_buf}{TIME_UNITS[word]}')
                txt_buf = None
                num_buf = None
                continue

        # Тут хендлим всё, что не попадает под модель "число указатель" или "указатель число"
        if time == today() and num_buf is not None:
            num_buf: int = int(num_buf)  # TODO: Опасное место, может правоцировать много ошибок. Нужно проработать
            time += datetime.timedelta(
                hours=num_buf if num_buf >= 12 else num_buf + 12)

    return time


print(parse_time('3 часа 10 минут'))
