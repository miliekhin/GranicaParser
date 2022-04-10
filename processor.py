import random
import re

from palka import (
    palka_detector,
    get_cars_count_by_word,
    find_range_value,
    PUSTO,
    PUSTO_FAKE,
    NA_ZAEZD,
    CARS_COUNT_WORDS
)
from cleaner import Cleaner
from combinator import Combinator
from combinator import KPP as comb_KPP

cleaner = Cleaner()
comb = Combinator()

KPP_NAMES = ('Успенка', 'Мариновка', 'Новоазовск', )

PRE_SPAM = (
    'пусто?', 'нет?', 'нету?', 'там?', 'машин?', 'машин ?',
)

SPAM = (
    'добро пожаловать', 'при поддержке', 'спасибо', 'подскаж', 'пожалуйста', 'прода', 'подвез', 'завтр', 'сутки',
    'faberli', 'дпс', 'экипаж', 'пакет', 'мы', 'скажите', 'протяжка', 'за час', 'в час', 'ваша репутац', 'груз 200',
    'груз200', 'одесская', 'что происходит', 'такси', 'ребен', 'ребён', 'электричк', 'билет', 'паспорт', 'регистр',
    'иловайск', 'товар', 'личку', 'привез', 'как обстановка', 'какая обстановка', 'одни пишут', 'пропускная способн',
    'образец', 'друзья пишите смс', 'вчера ехал', 'прошел границ', 'прошли границу', 'прошли за', 'проехали за',
    'проехал за', 'сейчас стою', 'сейчас стоим', 'читайте', 'стою на поворот', 'стою за поворот', 'кутейник',
    'назад был', 'пусто?', 'попутчик', 'выезжа', 'документ', 'между границам', 'заезжал', 'комсомольск', 'старобешев',
    'стоим с', 'проехали метров', 'посыл', 'помощ', 'забрать', 'пятёр', 'регион', 'возраст', 'телефон', 'призыв',
    'лисич', 'вчера никого',
)

KPP = ('успен', 'упенк', 'новоа', 'новао', 'новоо', 'марин', 'днр', 'рф', 'кург', 'вознес', 'вознис', 'куйб',)

NEUTRALKA = ('нейтр', 'тралк', 'серая', 'серой', 'под навесом', 'внутри', 'буфер',
             'зелен', 'зелён', 'нуле', 'ноле', 'промзон', 'терминал',
             )


def randomize_cars_count(cars):
    if cars:
        cars += random.randint(1, 2)
        if cars < 0:
            cars = 0

    return cars


def cars_count_by_object(message, kpp, way):
    if kpp == KPP_NAMES[0]:  # Успенка
        if way == 'to_dnr':
            if any(w in message for w in ('гостиниц', 'до столов',)):
                return 40
            if 'до мойк' in message:
                return 55
            if 'до поворот' in message:
                return 20
            if 'заправк' in message:
                return 69
            if 'за поворот' in message:
                digits = re.findall(r'\b\d+', message)
                if len(digits) > 1:  # many digit values
                    return None
                if len(digits) == 1:
                    return 20 + int(digits[0])
                else:
                    return 22
        if way == 'to_rf':
            if 'за заправк' in message:
                return 66
            if any(w in message for w in ('заправк', 'азс', )):
                return 45
            if 'склад' in message:
                return 88

    if kpp == KPP_NAMES[1]:
        if way == 'to_rf':
            if 'куст' in message:
                return 40

    if kpp == KPP_NAMES[2]:  # новоазовск
        if way == 'to_dnr':
            if any(w in message for w in ('за заправ', 'за луко', )):
                return 66
            if any(w in message for w in ('заправк', 'луко', )):
                return 55
            if 'до поворот' in message:
                return 22

    return None


def get_cars_type(message):
    if 'легков' in message:
        return 0

    if any(w in message for w in ('грузов', 'фур', )):
        return 1

    return 0


def parse_cars_by_words(message):
    words = '|'.join([*CARS_COUNT_WORDS])
    res = re.findall(fr'(?:{words}?\s?-?\s?)?легков\S+(?:\s?-?\s?{words})?', message)
    if len(res) == 1:
        res = re.findall(fr'{words}', res[0])
        if len(res) > 1:
            res = None
        elif len(res) == 1:
            res = CARS_COUNT_WORDS[res[0]]
        else:
            res = -1

    return res


def parse_cars(message):
    res = re.findall(r'(?:\d+?\s?-?\s?)?легков\S+(?:\s?-?\s?\d+)?', message)
    if len(res) == 1:
        res = re.findall(r'\d+', res[0])
        if len(res) == 1:
            res = int(res[0])
        elif len(res) > 1:
            res = None
        else:
            res = parse_cars_by_words(message)
    elif len(res) > 1:
        res = None
    else:
        res = -1

    if res is None:
        print('Many values for cars.')

    return res


def get_cars_count(message, kpp, way):
    pc = parse_cars(message)
    if pc is None:
        return None
    elif pc != -1:
        return pc

    cars = palka_detector(message)
    if cars is not None:
        return int(cars)

    cars = cars_count_by_object(message, kpp, way)
    if cars is not None:
        return int(cars)

    if any(c in message for c in NA_ZAEZD):
        return 0

    if any(c in message for c in PUSTO) and not any(c in message for c in PUSTO_FAKE):
        return 0

    if any(c in message for c in NEUTRALKA):
        # если есть инфа про нейтралку
        return None

    cars_range_value = find_range_value(message)
    # print('Range value:', cars_range_value)
    if cars_range_value is not None:
        return cars_range_value

    cbw = get_cars_count_by_word(message)
    # иначе ищем просто цифры
    digits = re.findall(r'\b\d+', message)

    if all((cbw, digits)) or len(digits) > 1:
        print('Unable to recognize: Many numbers in message')
        return None

    digits = int(digits[0]) if len(digits) == 1 else None
    cars = cbw if cbw else digits
    return cars


def get_kpp(message):
    if any(w in message for w in ('успен', 'кург', 'матвее', )):
        return KPP_NAMES[0]
    if any(w in message for w in ('новоа', 'новао', 'новоо', 'новоз', 'вознес', )):
        return KPP_NAMES[2]
    if any(w in message for w in ('марин', 'куйб', )):
        return KPP_NAMES[1]
    return ''


def get_way(message):
    way = ''
    words = '|'.join([*comb_KPP])
    res = re.findall(fr'{words}', message)
    if len(res) > 1:
        print('Many KPP names in message')
        return way

    if any(c in message for c in comb.TO_DNR_KPPS):
        way = 'to_dnr'
    elif any(c in message for c in comb.TO_RF_KPPS):
        way = 'to_rf'

    if not way:
        if any(c in message for c in comb.TO_DNR):
            way = 'to_dnr'
        elif any(c in message for c in comb.TO_RF):
            way = 'to_rf'

    if not way:
        if any(c in message for c in comb.TO_DNR2):
            way = 'to_dnr'
        elif any(c in message for c in comb.TO_RF2):
            way = 'to_rf'

    if not way:
        if get_kpp(message):
            way = 'to_rf'

    return way


def is_message_ready_to_parse(message):
    if len(message) < 5:
        print('Too short message.')
        return False
    for c in SPAM:
        if c in message:
            print(f'Spam detected: {c}')
            return False
    if not any(c in message for c in KPP):
        print('KPP is not present')
        return False
    if message[-1] == '?':
        print('? at the end of message')
        return False
    return True


def word_num_separator(msg):
    """Разделение слитых слов и цифр"""
    res = []
    for w in msg.split():
        sep = re.findall(r'[а-яё\-]+|\d+', w)
        res += sep
    line = ' '.join(res)
    return line


def get_valid_data(message):
    print('\n--------------------------------')
    print('Original message:', message)
    # low_message = message.lower().replace('c', 'с').replace('  ', ' ')
    msg_for_way_parser = message.lower().replace('c', 'с')

    if message.count('?') > 1:
        print('Many question marks found.')
        return None

    if any(c in message for c in PRE_SPAM):
        print('Prespam detected.')
        return None

    low_message = cleaner.clear_rational_number(msg_for_way_parser)
    low_message = word_num_separator(low_message)
    low_message = cleaner.clean(low_message)
    print('Processed message:', low_message)

    valid_data = dict()
    print('CHECK is_message_ready_to_parse')
    res = is_message_ready_to_parse(low_message)
    print('RESULT:', res)
    if not res:
        return None

    print('CHECK get_way')
    way = get_way(msg_for_way_parser)
    print('RESULT:', way)
    if len(way) == 0:
        return None
    valid_data['way'] = way

    print('CHECK get_kpp')
    kpp = get_kpp(low_message)
    print('RESULT:', kpp)
    if len(kpp) == 0:
        return None
    valid_data['kpp_name'] = kpp

    print('CHECK get_cars_count')
    cars = get_cars_count(low_message, kpp, way)
    print('RESULT:', cars)
    if cars is None or cars > 1024:
        return None

    valid_data['cars_num'] = randomize_cars_count(cars)

    valid_data['comment'] = message
    print('CHECK get_cars_type')
    valid_data['car_type'] = get_cars_type(low_message)
    print('RESULT:', valid_data['car_type'])
    # print('Valid data:', valid_data, '\n')
    return valid_data
