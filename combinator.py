import itertools

RF = ('р.ф.', 'р.ф', 'рф', '🇷🇺', 'россия', 'рос', )
FROM = ('с', 'из', 'со стороны', )
TO = ('в', '➡',  '▶️', '>', '-', '_', '/', 'на', 'ы', '⏩', '➡️', '—', )
KPP = ('ново', 'успен', 'марин', )
KPP_ENDS_DNR = ('зовск', 'пенка', 'иновка', 'иночка',)
KPP_ENDS_RF = ('курган', 'бышево', 'несенка',)
STORONU = ('сторону ', 'строну ', )
DNR = ('днр', 'донецк', )
EXTRA_TO_DNR = ('матвее', 'курган', 'куйб', 'вознес', 'в сторону дома', 'домой', )
EXTRA_TO_RF = ('на россию', 'на выезд', )


def add_r_space(tpl):
    return tuple(e + ' ' for e in tpl)


def add_l_space(tpl):
    return tuple(' ' + e for e in tpl)


def add_lr_space(tpl):
    return tuple(' ' + e + ' ' for e in tpl)


def combine_spaces(tpl):
    return tpl + add_r_space(tpl) + add_l_space(tpl) + add_lr_space(tpl)


def to_dnr2():
    """
    Было добавлено после случая "Успенка ДНР РФ 13 машин" определилось как to_dnr
    """
    kpp_dnr = [''.join(s) for s in itertools.product(KPP_ENDS_DNR, add_l_space(DNR))]
    return kpp_dnr


def to_dnr():
    rf_dnr = [''.join(s) for s in itertools.product(add_r_space(RF), DNR)]
    rf_v_dnr = [''.join(s) for s in itertools.product(RF, combine_spaces(TO), DNR)]
    from_rf_kpp = [''.join(s) for s in itertools.product(FROM + add_r_space(FROM), RF, combine_spaces(TO), KPP)]
    storonu_kpp = [''.join(s) for s in itertools.product(STORONU, KPP)]
    storonu_dnr = [''.join(s) for s in itertools.product(STORONU, DNR)]
    iz_rf = [''.join(s) for s in itertools.product(FROM + add_r_space(FROM), RF)]
    v_dnr = [''.join(s) for s in itertools.product(TO[:5] + add_r_space(TO[:5]), DNR)]
    # print(rf_dnr, '\n')
    # print(rf_v_dnr, '\n')
    # print(rf_kpp, '\n')
    # print(storonu_kpp, '\n')
    # print(storonu_dnr, '\n')
    # print(iz_rf, '\n')
    # print(v_dnr, '\n')
    result = tuple(rf_dnr + rf_v_dnr + from_rf_kpp + storonu_kpp + iz_rf + v_dnr + storonu_dnr) + EXTRA_TO_DNR
    # print(result)
    return result


def to_rf2():
    kpp_rf = [''.join(s) for s in itertools.product(KPP_ENDS_DNR, add_l_space(RF))]
    return kpp_rf


def to_rf():
    dnr_rf = [''.join(s) for s in itertools.product(add_r_space(DNR), RF)]
    dnr_v_rf = [''.join(s) for s in itertools.product(DNR, combine_spaces(TO), RF)]
    kpp_v_rf = [''.join(s) for s in itertools.product(KPP_ENDS_DNR, combine_spaces(TO), RF)]
    v_storonu_rf = [''.join(s) for s in itertools.product(STORONU, RF)]
    to_rf_ = [''.join(s) for s in itertools.product(TO + add_r_space(TO), RF)]
    na_vyezd = [''.join(s) for s in itertools.product(KPP_ENDS_DNR, add_l_space(EXTRA_TO_RF))]
    iz_dnr = [''.join(s) for s in itertools.product(FROM + add_r_space(FROM), DNR)]

    # print(dnr_v_rf, '\n')
    # print(v_storonu_rf, '\n')
    # print(to_rf_, '\n')
    # print(na_vyezd, '\n')
    # print(iz_dnr, '\n')
    result = tuple(dnr_v_rf + v_storonu_rf + to_rf_ + na_vyezd + iz_dnr + kpp_v_rf + dnr_rf)
    # print(result)
    return result


def to_rf_kpps():
    kpp_v_kpp = [''.join(s) for s in itertools.product(KPP_ENDS_DNR, combine_spaces(TO), EXTRA_TO_DNR)]
    result = tuple(kpp_v_kpp)
    return result


def to_dnr_kpps():
    kpp_v_kpp = [''.join(s) for s in itertools.product(KPP_ENDS_RF, combine_spaces(TO), KPP)]
    result = tuple(kpp_v_kpp)
    return result


class Combinator:
    def __init__(self):
        self.TO_DNR_KPPS = to_dnr_kpps()
        self.TO_RF_KPPS = to_rf_kpps()
        self.TO_DNR = to_dnr()
        self.TO_RF = to_rf()
        self.TO_DNR2 = to_dnr2()
        self.TO_RF2 = to_rf2()
