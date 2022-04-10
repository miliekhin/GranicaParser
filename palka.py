import re
import itertools
from combinator import add_r_space

PREFX_BEFORE = ('до ', 'перед ', 'под ', 'на ', )
PALKA = ('шлакб', 'шлагб', 'палк', 'въезд')
CARS_WORDS = ('машин', 'авто',)
CARS_COUNT_WORDS = {'одна': 1, 'два ': 2, 'две ': 2, 'пара ': 2, 'пару ': 2, 'три ': 3, 'четыре': 4,
                    'пять': 5, 'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10, 'мало машин': 5}

MINUSES = ('-', ' - ', '- ', ' -', )

PUSTO = ('никого', 'некого', 'ни кого', 'пусто', 'ноль', 'нуль', 'машин нет', 'нет машин', 'свободно', )

PUSTO_FAKE = ('ноль забит', 'ноль полный', )

NA_ZAEZD = (
    'сразу на заезд', 'сразу заезд', 'сразу на въезд', 'сразу под навес', 'сразу заехали под навес', 'очереди нет',
    'пусто на въезд', 'баумом никого', 'сразу на досмотр', 'сразу въезд', 'сразу заехал под навес', 'запустили сразу',
)
PALKA_WORD = ('палк', 'шлагбаум', 'шлакбаум',)
PALKA_SUFFIX = ('е', 'ом', 'ой', 'а',)

palka_word_null = [''.join(s) for s in itertools.product(add_r_space(PALKA_WORD), PUSTO)]
palka_words = [''.join(s) for s in itertools.product(PALKA_WORD, PALKA_SUFFIX)]
null_pered_palka = [''.join(s) for s in itertools.product(add_r_space(PUSTO), PREFX_BEFORE, palka_words)]
palka_word_0 = [''.join(s) for s in itertools.product(add_r_space(PALKA_WORD), '0')]
palka_words_0 = [''.join(s) for s in itertools.product(add_r_space(palka_words), '0')] + palka_word_0
palka_null = [''.join(s) for s in itertools.product(add_r_space(palka_words), PUSTO)]
palka_combs = palka_null + palka_word_null + palka_words_0 + null_pered_palka


def find_range_value(message):
    arr_digits = re.findall(r'\b\d+', message)
    cars = None

    if len(arr_digits) == 2:
        digit_low = int(arr_digits[0])
        digit_high = int(arr_digits[1])

        i1 = message.find(arr_digits[0])
        i2 = message.find(arr_digits[1])
        txt_between_digits = message[i1 + len(arr_digits[0]): i2]
        if txt_between_digits in MINUSES:
            average = abs(round((digit_high - digit_low) / 2))
            if digit_low < digit_high:
                cars = digit_low + average
            else:
                cars = digit_high + average

    return cars


def get_cars_count_by_word(message):
    cars = None
    for word in [*CARS_COUNT_WORDS]:
        indxs = [i.start() for i in re.finditer(word, message)]
        if len(indxs) > 1:
            return None
        elif len(indxs) == 1:
            if cars:
                return None

            cars = CARS_COUNT_WORDS[word]

    return cars


def _find_cars_in_words(finded_cars_words_arr):
    # print('finded_cars_words_arr:', finded_cars_words_arr)
    cars_count = None
    cars_word_detected = False
    for car_word in CARS_WORDS:
        for w in finded_cars_words_arr:
            if w.find(car_word) == -1:  # если слово машин не найдно
                w = w.replace(',', '').replace('.', '')
                if w.isdigit():
                    cars_count = w
                else:
                    w = w[:-1] if any(w.endswith(x) for x in ('.', ',')) else w
                    if w in PUSTO:
                        cars_count = 0
                    elif cars_count is None:
                        cars_count = find_range_value(w)
            elif cars_count:
                cars_word_detected = True

        if cars_count is not None:
            break

    return cars_count, cars_word_detected


def palka_detector(message):
    """Распознавание подстроки 'Перед палкой/шлагбаумом' """
    cars_count = None
    if any(c in message for c in palka_combs):
        cars_count = 0

    res = re.findall(r'(?:палка|шла[гк]баум) \d+', message)
    if len(res) == 1:
        cars_count = re.search(r'\b\d+', res[0]).group(0)
        # cars_count = int(res[0].replace('палка ', ''))

    if cars_count is None:
        na_palke = [''.join(s) for s in itertools.product(PREFX_BEFORE, PALKA)] + list(PALKA)
        # print(na_palke)
        for subtxt in na_palke:
            find_idx = message.find(subtxt)  # ищем слова про палку или шлагбаум
            if find_idx > -1:  # если нашлись - ищем предыдущие 2 слова
                cars_before, ok_cb = _find_cars_in_words(message[:find_idx].split()[-2:])
                cars_after, ok_ca = _find_cars_in_words(message[find_idx:].split()[2:4])
                if all((cars_before is not None, cars_after is not None)):
                    break
                if not all((ok_ca, ok_cb)):
                    cars_count = cars_before if ok_cb else cars_after
                    if cars_count is not None:
                        break
                # if not all((cars_after is not None, cars_before is not None)):
                #     cars_count = cars_after if cars_after is not None else cars_before

    print('Palka detector:', cars_count)
    return cars_count
