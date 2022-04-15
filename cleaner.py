import itertools
import re

from combinator import add_r_space

VSE = (
    'вся ', 'все ', 'всё ', 'весь ',
)
PREFIX = (
    'ноль', 'нейтральной полосе', 'нейтральная полоса', 'под навесом', 'навесе', 'навес', 'нейтралка',
    'нейтральная', 'нейтральной', 'нетралка', 'нитралка', 'нейтралке', 'нетралке', 'буфер', 'буфере',
    'нейтраль', 'нейтрале', 'нейтрали', 'серая', 'серая зона', 'буферная зона', 'серой', 'серой зоне', 'буферной зоне',
    'промзона', 'промзоне', 'нулевик', 'нулевой', 'терминале', 'терминал',
)
MIDDLE = (
    'битком', 'забито', 'забита', 'забитый', 'полно', 'полный', 'полная', 'пустой', 'пустая', 'пусто', 'забит',
    'битком', 'есть', 'никого',
)
AUX = (
    'один ряд', 'два ряда', '1 ряд', '2 ряд', '2 рчда', '3 ряда', '4 ряда', 'две границы', 'обе границы',
    'навес и ноль', 'две таможни', 'две полосы', 'три полосы', 'одна полоса', 'движение ноль', 'движения ноль',
    'был пустой', 'было пусто', 'движение 0', 'движения 0', 'две очереди', 'три очереди', 'одна очередь', 'смотри',
    'пусто?', '0 забит', 'одна за одной', 'перед навесом', 'никого не пропускают', 'никого не разворачивают',
    '2 таможни', 'фуры и автобусы', 'впускают фуры', 'опять', 'пустой багажник', 'три поста', 'до 65', 'до 55',
)
DIGITS = (
    'одна', 'одну', 'две', 'пару', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'сем', 'восемь', 'восем',
    'девять', 'десять',
)
TIME = (
    'часа', 'часа на', 'часов', 'час', 'минуты', 'минут', 'мин', 'ч', 'утра', 'вечера', 'месяца', 'года',
)
TRUCKS = (
    'грузовая', 'грузовых', 'фура', 'фуры', 'фур', 'грузовиков', 'очень много'
)
MANY = (
    'до фига', 'дофига', 'много', 'немеренно', 'немеряно', 'немерянно', 'нимеряно', 'далеко',
)
KM = (
    'км', 'километр', 'человека', 'минут', 'час',
)
PRODVIN = (
    'продвинулись', 'продвинулось', 'продвинулась', 'метров',
)
RE_OTHER = (
    r'\d+ под навесом$', r'навес(ом)? \d+$', r'в (серой зоне|н[еи][йи]?тралке) \d+', r'семь[я|ё|е]',
    r'(льгота|н[еи][йи]?тралка|навес) \d+', r'ноль.+забит', r'(человек|км|километров|метров) \d+( - \d+)?',
    r'(?:\d+\s?-?\s?\d+)\s(челов|прошл|лет)', r'\d+\s?(девоч|детей|женщин|муж)', r'(мне|ему)\s?\d+\s?[лет]?',
    r'мужчин[ы]? до\s?\d+', r'нейтралк(а|е) (около|до)\s?\d+', r'был[о|и]\s?\d+', r'\d+ р', r'в \d+ ехал',
    r'запустили\s?(\d+|\d+ - \d+)\s?машин', r'\d+\s?(лет|год|автобус|мест|сторон|процент|суток)', r'в \d+ - \d+',
    r'\d+ (янв|февр|март|апре|мая|июн|июл|авгус|сентяб|октяб|нояб|декаб)',  r'движемся по (?:\d+ - \d+|\d+)',
    r'пеш[е|и]х(?:одов)? (около|до|бол(ьше|ее))?\s?(чем)?\s?\d+',
)
DIFF = (
    'мест', 'раз', 'девоч', 'детей', 'женщин', 'муж', 'ребен', 'ребён', 'парн', 'ребят',
)


class Cleaner:
    combinations = ()

    def __init__(self):
        combs = [''.join(s) for s in itertools.product(add_r_space(PREFIX), MIDDLE)]
        combs_vse = [''.join(s) for s in itertools.product(add_r_space(PREFIX), VSE, MIDDLE)]
        combs_dt = [''.join(s) for s in itertools.product(add_r_space(DIGITS), TIME)]
        combs_km = [''.join(s) for s in itertools.product(add_r_space(DIGITS), KM)]
        combs_diff = [''.join(s) for s in itertools.product(add_r_space(DIGITS), DIFF)]
        combs_td = [''.join(s) for s in itertools.product(add_r_space(TIME), DIGITS)]
        combs_prodv = [''.join(s) for s in itertools.product(add_r_space(PRODVIN), DIGITS)]
        combs_prodv_na = [''.join(s) for s in itertools.product(add_r_space(PRODVIN), add_r_space(('на',)), DIGITS)]
        self.combs_gruz = [''.join(s) for s in itertools.product(add_r_space(DIGITS), TRUCKS)]
        combs_many_trucks = [''.join(s) for s in itertools.product(add_r_space(MANY), TRUCKS)]
        combs_trucks_many = [''.join(s) for s in itertools.product(add_r_space(TRUCKS), MANY)]

        self.combinations = tuple(combs + combs_vse + combs_td + combs_dt + combs_km + combs_prodv +
                                  combs_prodv_na + combs_diff + combs_many_trucks + combs_trucks_many) + AUX

        km = '|'.join(KM)
        self.re_other = RE_OTHER + (fr'(?:\d+ - \d+|\d+) (?:{km})', )

    @staticmethod
    def clear_prodvin(msg):
        prodv = '|'.join((tuple([''.join(s) for s in itertools.product(add_r_space(PRODVIN), ('на', 'в'))]) + PRODVIN))
        ret = re.sub(fr'(?:{prodv}) \d+', '', msg).replace('  ', ' ')
        return ret

    def clear_other(self, msg):
        ret = re.sub('|'.join(self.re_other), '', msg).replace('  ', ' ')
        return ret

    def clear_trucks(self, msg):
        trucks = '|'.join(TRUCKS)
        ret = re.sub(fr'\d+ (?:{trucks})', '', msg).replace('  ', ' ')
        for item in self.combs_gruz:
            i = ret.find(item)
            if i != -1:
                ret = ret.replace(item, '')
        return ret

    @staticmethod
    def clear_times(msg):
        times = '|'.join(TIME)
        msg = re.sub(fr'\d+ (?:{times})', '', msg).replace('  ', ' ')
        msg = re.sub(fr'(?:{times}) \d+', '', msg).replace('  ', ' ')
        msg = re.sub(fr'с \d+ - \d+', '', msg).replace('  ', ' ')
        return msg

    @staticmethod
    def clear_rational_number(msg):
        msg = re.sub(r'\d+[,.:/]\d+', '', msg).replace('  ', ' ')
        ret = re.sub(r'\d+/', '', msg).replace('  ', ' ')
        return ret

    def clean(self, msg):
        all_combs = '|'.join(self.combinations)
        res = re.findall(fr'\d+ (?:{all_combs}) \d+', msg)
        if len(res):  # только если нашлись комбинации \d+ фраза \d+
            print('Clean exception finded')
            return msg

        # msg = self.clear_trucks(msg)
        msg = self.clear_prodvin(msg)
        msg = self.clear_other(msg)
        msg = self.clear_times(msg)

        for item in self.combinations:
            i = msg.find(item)
            if i != -1:
                msg = msg.replace(item, '')

        return msg
